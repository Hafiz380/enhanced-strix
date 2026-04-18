
# 🎯 Bug Bounty Hunter's Guide to Strix

Strix is your ultimate partner for scaling security research. Here’s how to maximize your bounty hunt using the new **Vulnerability Verification System**.

## 🚀 Scaling Your Workflow
Strix automates the boring parts of hunting: recon, payload spraying, and impact verification.

### 1. Advanced Recon & Scan
```bash
strix scan --target https://vulnerable-site.com --scan-mode deep
```
Strix will map the attack surface and automatically try complex vectors like SSRF and IDOR.

### 2. Automatic Verification
Strix doesn't just report "Possible XSS." It attempts to trigger a safe alert and captures:
- **Reproduction Steps**: Copy-pasteable commands for your report.
- **Practical POC**: A Python script you can attach as evidence.
- **Impact Proof**: Screenshots or logs showing sensitive data access.

## 💎 Maximizing Payouts
Bounty programs pay for **Impact**. Strix helps you prove it:
- **Data Leak Extraction**: If an IDOR is found, Strix will identify what PII could be leaked.
- **Real-life Demonstration**: Strix writes a narrative of how an attacker would exploit the chain.
- **Zero False Positives**: With the 95% verification mandate, your reports are high-signal.

## 🛠️ Tips for Hunters
- **Custom Instructions**: Tell Strix where to look.
  `strix scan -t target.com --instruction "Focus on the /api/v2/admin endpoints"`
- **Monitor Stats**: Check your efficiency with `strix stats`.
- **Review Artifacts**: Look in `strix_runs/[run_name]/artifacts` for detailed logs and evidence.

---
*Happy Hunting! 🦊*
