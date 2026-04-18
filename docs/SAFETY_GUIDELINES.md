
# 🛡️ Safety & Ethical Guidelines for Strix

Strix is a powerful autonomous AI security auditor. To ensure responsible usage and prevent accidental damage, follow these guidelines.

## 1. Authorized Scope Only
- **NEVER** scan targets without explicit written permission.
- Ensure all domains, IPs, and repositories are within your authorized scope.
- Strix is designed for "Internal Engineering" and "Bug Bounty" contexts.

## 2. Risk Assessment & POCs
Strix includes an automated **Risk Assessment** mechanism:
- **Destructive Payloads**: By default, Strix avoids payloads that could cause Data Loss or Denial of Service (DoS).
- **Practical Verification**: If a bug is marked as `Critical` or `Unsafe`, Strix will provide a "Theoretical POC" instead of executing it live.
- **Safe Mode**: Use `--scan-mode standard` for a more conservative approach compared to `--scan-mode deep`.

## 3. Handling Sensitive Data
- Strix automatically classifies PII (Emails, JWTs, API Keys) during verification.
- In reports, sensitive data is **MASKED** (e.g., `ad****om`).
- **Do NOT** share raw artifacts containing unmasked production data.

## 4. Operational Safety
- Run Strix in a **Docker Sandbox** (default behavior) to isolate its execution.
- Monitor terminal logs for unexpected tool behavior.
- Use `Ctrl+C` to immediately terminate all agent activities if you notice an out-of-scope request.

## 5. Compliance
- Adhere to local laws (e.g., Computer Misuse Act, GDPR).
- For Bug Bounty: Follow the program's specific "Rules of Engagement."

---
*OmniSecure Labs - Building a safer web through autonomous intelligence.*
