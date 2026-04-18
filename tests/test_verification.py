
import pytest
import asyncio
from strix.verification.engine import VerificationEngine
from strix.utils.data_classifier import DataClassifier

@pytest.mark.asyncio
async def test_verification_engine():
    engine = VerificationEngine()
    vuln = {
        "id": "VULN-001",
        "type": "SQL Injection",
        "severity": "High",
        "target": "http://example.com/api/user"
    }
    
    result = await engine.verify_vulnerability(vuln)
    
    assert result.vuln_id == "VULN-001"
    assert result.is_verified is True
    assert result.risk_level == "High"
    assert result.is_poc_safe is True
    assert "import requests" in result.reproduction_script

def test_data_classifier():
    classifier = DataClassifier()
    sample_text = "Contact me at admin@example.com or use key: sk-abcdef12345678901234"
    
    results = classifier.classify(sample_text)
    
    assert "email" in results
    assert "ad****om" in results["email"]
    assert "api_key" in results
    assert classifier.contains_sensitive_data(sample_text) is True
    assert classifier.contains_sensitive_data("Clean text") is False
