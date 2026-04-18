import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class TokenReporter:
    """Handles token usage reporting and persistence."""

    def __init__(self, report_dir: Optional[Path] = None):
        if report_dir is None:
            self.report_dir = Path.home() / ".strix" / "stats"
        else:
            self.report_dir = report_dir
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.stats_file = self.report_dir / "token_usage.json"

    def load_stats(self) -> Dict[str, Any]:
        if not self.stats_file.exists():
            return {
                "total_input_tokens": 0,
                "total_output_tokens": 0,
                "total_cached_tokens": 0,
                "total_cost": 0.0,
                "total_requests": 0,
                "sessions": []
            }
        try:
            with self.stats_file.open("r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    def save_session_stats(self, session_id: str, stats: Dict[str, Any]) -> None:
        all_stats = self.load_stats()
        
        all_stats["total_input_tokens"] += stats.get("input_tokens", 0)
        all_stats["total_output_tokens"] += stats.get("output_tokens", 0)
        all_stats["total_cached_tokens"] += stats.get("cached_tokens", 0)
        all_stats["total_cost"] += stats.get("cost", 0.0)
        all_stats["total_requests"] += stats.get("requests", 0)
        
        session_entry = {
            "session_id": session_id,
            "timestamp": os.path.getmtime(self.stats_file) if self.stats_file.exists() else 0,
            **stats
        }
        all_stats["sessions"].append(session_entry)
        
        # Keep only last 50 sessions
        if len(all_stats["sessions"]) > 50:
            all_stats["sessions"] = all_stats["sessions"][-50:]
            
        try:
            with self.stats_file.open("w", encoding="utf-8") as f:
                json.dump(all_stats, f, indent=2)
        except OSError:
            pass

    def generate_report(self) -> str:
        from strix.config.settings_manager import SettingsManager
        sm = SettingsManager()
        
        stats = self.load_stats()
        report = [
            "========================================",
            "        STRIX PERFORMANCE REPORT        ",
            "========================================",
            f"Total Requests:      {stats.get('total_requests', 0)}",
            f"Total Input Tokens:  {stats.get('total_input_tokens', 0):,}",
            f"Total Output Tokens: {stats.get('total_output_tokens', 0):,}",
            f"Total Cached Tokens: {stats.get('total_cached_tokens', 0):,}",
            f"Total Estimated Cost: ${stats.get('total_cost', 0.0):.4f}",
            "----------------------------------------",
            "Active API Endpoints:",
        ]
        
        if sm.configs:
            for cfg in sorted(sm.configs, key=lambda x: x.priority):
                status = "🟢 Ready" if cfg.failures < 3 else "🔴 Disabled"
                latency = f"{cfg.latency:.2f}s" if cfg.latency != float('inf') else "N/A"
                report.append(f"- {cfg.name:<16} | {cfg.model:<24} | {status} | Latency: {latency}")
        else:
            report.append("  (No endpoints configured)")
            
        report.extend([
            "========================================",
            "Recent Sessions:",
        ])
        
        for s in stats.get("sessions", [])[-5:]:
            report.append(f"- Session {s['session_id'][:8]}: {s.get('input_tokens', 0)} in / {s.get('output_tokens', 0)} out / ${s.get('cost', 0.0):.4f}")
            
        return "\n".join(report)
