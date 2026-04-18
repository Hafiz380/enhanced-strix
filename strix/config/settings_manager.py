import base64
import json
import os
import time
import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Optional, Dict, List
import logging

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

logger = logging.getLogger(__name__)


@dataclass
class APIConfig:
    """Represents a single API configuration."""
    name: str
    model: str
    api_key: str
    api_base: Optional[str] = None
    priority: int = 100
    latency: float = float('inf')  # Track average response time
    failures: int = 0  # Count consecutive failures
    last_used: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SettingsManager:
    """Manages secure API settings with failover and multi-config support."""

    def __init__(self, config_dir: Optional[Path] = None):
        if config_dir is None:
            self.config_dir = Path.home() / ".strix"
        else:
            self.config_dir = config_dir
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "secure-settings.json"
        self.key_file = self.config_dir / ".key"
        self._fernet = self._init_encryption()
        self.configs: List[APIConfig] = self._load_configs()
        
        # Load external config (YAML/JSON) if present
        self.load_external_config()

    def _init_encryption(self) -> Fernet:
        """Initialize encryption key based on machine-specific or persistent key."""
        if not self.key_file.exists():
            # Generate a new key if it doesn't exist
            key = Fernet.generate_key()
            with self.key_file.open("wb") as f:
                f.write(key)
        else:
            with self.key_file.open("rb") as f:
                key = f.read()
        return Fernet(key)

    def _encrypt(self, text: str) -> str:
        """Encrypt a string."""
        return self._fernet.encrypt(text.encode("utf-8")).decode("utf-8")

    def _decrypt(self, encrypted_text: str) -> str:
        """Decrypt a string."""
        return self._fernet.decrypt(encrypted_text.encode("utf-8")).decode("utf-8")

    def _load_configs(self) -> List[APIConfig]:
        """Load API configurations from file."""
        if not self.config_file.exists():
            return []
        
        try:
            with self.config_file.open("r", encoding="utf-8") as f:
                data = json.load(f)
                configs = []
                for item in data.get("api_configs", []):
                    # Decrypt sensitive data
                    item["api_key"] = self._decrypt(item["api_key"])
                    configs.append(APIConfig(**item))
                return configs
        except (json.JSONDecodeError, OSError, Exception):
            return []

    def save_configs(self) -> bool:
        """Save current API configurations to file."""
        try:
            data = {"api_configs": []}
            for cfg in self.configs:
                item = cfg.to_dict()
                # Encrypt sensitive data
                item["api_key"] = self._encrypt(item["api_key"])
                data["api_configs"].append(item)
                
            with self.config_file.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            try:
                self.config_file.chmod(0o600)  # Restrict access
            except Exception:
                pass # May fail on Windows
            return True
        except (OSError, Exception):
            return False

    def add_config(self, name: str, model: str, api_key: str, api_base: Optional[str] = None, priority: int = 100) -> bool:
        """Add a new API configuration."""
        # Check if already exists
        for cfg in self.configs:
            if cfg.name == name:
                cfg.model = model
                cfg.api_key = api_key
                cfg.api_base = api_base
                cfg.priority = priority
                return self.save_configs()
        
        self.configs.append(APIConfig(name=name, model=model, api_key=api_key, api_base=api_base, priority=priority))
        return self.save_configs()

    def load_external_config(self) -> None:
        """Load and merge configuration from external YAML/JSON file if present."""
        try:
            import yaml
        except ImportError:
            return # YAML support requires PyYAML

        # Possible locations for external config
        root_dir = Path(__file__).parent.parent.parent # Project root
        possible_paths = [
            root_dir / ".config" / "api-config.yaml",
            root_dir / "api-config.yaml",
            root_dir / "endpoints.json"
        ]
        
        for path in possible_paths:
            if path.exists():
                try:
                    with path.open("r", encoding="utf-8") as f:
                        if path.suffix in [".yaml", ".yml"]:
                            data = yaml.safe_load(f)
                        else:
                            data = json.load(f)
                            
                        if not data or "endpoints" not in data:
                            continue
                            
                        for ep in data["endpoints"]:
                            name = ep.get("name")
                            model = ep.get("model")
                            api_key = ep.get("api_key", "")
                            
                            # Expand environment variables if key is in ${VAR} format
                            if api_key and isinstance(api_key, str) and api_key.startswith("${") and api_key.endswith("}"):
                                env_var = api_key[2:-1]
                                api_key = os.getenv(env_var, api_key)
                            
                            if name and model:
                                self.add_config(
                                    name=name,
                                    model=model,
                                    api_key=api_key,
                                    api_base=ep.get("api_base"),
                                    priority=ep.get("priority", 100)
                                )
                except Exception as e:
                    logger.error(f"Failed to load external config from {path}: {e}")

    def get_best_config(self) -> Optional[APIConfig]:
        """Get the best API configuration based on latency, priority, and failure history."""
        if not self.configs:
            return None
            
        # Filter out configurations with too many failures
        active_configs = [c for c in self.configs if c.failures < 3]
        if not active_configs:
            # If all have failed, reset failures and try again
            for c in self.configs:
                c.failures = 0
            active_configs = self.configs
            
        # Sort by: 1. Failures (asc), 2. Latency (asc), 3. Priority (desc)
        sorted_configs = sorted(active_configs, key=lambda x: (x.failures, x.latency, -x.priority))
        return sorted_configs[0]

    def update_performance(self, name: str, latency: float, success: bool) -> None:
        """Update latency and failure statistics for a configuration."""
        for cfg in self.configs:
            if cfg.name == name:
                if success:
                    # Rolling average for latency
                    if cfg.latency == float('inf'):
                        cfg.latency = latency
                    else:
                        cfg.latency = (cfg.latency * 0.7) + (latency * 0.3)
                    cfg.failures = 0
                else:
                    cfg.failures += 1
                cfg.last_used = time.time()
                break
        self.save_configs()
