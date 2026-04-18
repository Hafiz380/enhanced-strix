
import os
from pathlib import Path
from datetime import datetime

class POCRecorder:
    """Handles recording of Proof-of-Concepts (Mock for Sandbox)."""
    
    def __init__(self, run_name: str):
        self.output_dir = Path(f"strix_runs/{run_name}/artifacts")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def record_screenshot(self, name: str, data: bytes):
        """Saves a screenshot artifact."""
        path = self.output_dir / f"{name}_{datetime.now().strftime('%H%M%S')}.png"
        path.write_bytes(data)
        return str(path)

    def record_terminal_output(self, name: str, content: str):
        """Saves terminal session output as a text artifact."""
        path = self.output_dir / f"{name}_{datetime.now().strftime('%H%M%S')}.log"
        path.write_text(content)
        return str(path)

    def generate_poc_package(self, vuln_id: str):
        """Creates a zip/folder package with all evidence."""
        # Simulated logic to package reproduction script + artifacts
        return f"Package generated at {self.output_dir}/{vuln_id}_poc.zip"
