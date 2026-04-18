
import re
from typing import Dict, List, Optional

class DataClassifier:
    """Classifies and detects sensitive information (PII, Secrets, etc.)."""
    
    PATTERNS = {
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "api_key": r"(?:key|api|token|secret|auth)[-_]?(?:id|key|token|secret|auth)?[:=]\s*['\"]?([a-zA-Z0-9\-_]{20,})['\"]?",
        "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        "aws_key": r"AKIA[0-9A-Z]{16}",
        "jwt": r"eyJh[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+",
        "credit_card": r"\b(?:\d[ -]*?){13,16}\b",
        "phone": r"\b\+?[0-9]{1,4}?[-. ]?\(?[0-9]{1,3}?\)?[-. ]?[0-9]{1,4}[-. ]?[0-9]{1,4}[-. ]?[0-9]{1,9}\b"
    }

    def classify(self, text: str) -> Dict[str, List[str]]:
        """Identifies and returns classified sensitive data found in text."""
        results = {}
        for label, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                # Mask the data for safety
                results[label] = [self._mask(m) for m in matches]
        return results

    def _mask(self, data: str) -> str:
        """Masks sensitive data for safe reporting."""
        if len(data) <= 4:
            return "****"
        return data[:2] + "****" + data[-2:]

    def contains_sensitive_data(self, text: str) -> bool:
        """Quick check if any sensitive pattern is present."""
        return any(re.search(p, text, re.IGNORECASE) for p in self.PATTERNS.values())
