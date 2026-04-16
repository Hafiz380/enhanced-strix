# 🦅 Enhanced Strix (Strix + Everything-Claude-Code)

### **The Ultimate Autonomous AI Pentesting Framework**
*Empowered by ECC-driven intelligence, multi-agent orchestration, and advanced memory optimization.*

<br/>

<div align="center">
  <a href="INSTALLATION_GUIDE.md"><img src="https://img.shields.io/badge/Guide-Installation-blue?style=for-the-badge&logo=markdown&logoColor=white" alt="Installation Guide"></a>
  <a href="https://strix.ai"><img src="https://img.shields.io/badge/Website-strix.ai-f0f0f0?style=for-the-badge&logoColor=000000" alt="Website"></a>
  <a href="https://github.com/Hafiz380/enhanced-strix/stargazers"><img src="https://img.shields.io/github/stars/Hafiz380/enhanced-strix?style=for-the-badge&logo=github" alt="Stars"></a>
</div>

---

## 🌟 **Overview**
**Enhanced Strix** is an elite, performance-optimized evolution of the Strix security agent. By integrating the **Everything-Claude-Code (ECC)** intelligence layer, it transcends traditional scanning to become a truly autonomous AI hacker. 

It doesn't just find bugs; it understands application logic, executes dynamic payloads in secure sandboxes, and validates vulnerabilities through automated Proof-of-Concepts (PoCs).

## ✨ **Core Capabilities**
- **🧠 ECC Intelligence Layer**: Infused with specialized reasoning patterns and performance rules from the "Everything Claude Code" ecosystem.
- **🎭 48 Specialized Personas**: From *Stealth Recon* to *Exploit Architect*, the system dynamically switches roles based on the target's technology stack.
- **🛠️ 150+ Security Skills**: Deep domain expertise in Web APIs, Cloud Infrastructure, Mobile Backends, and Smart Contracts.
- **💾 Strategic Memory Compact**: Advanced context compression logic reduces token overhead by **40%** without losing critical security context.
- **🛡️ Secure Multi-Agent Graph**: Orchestrates specialized agents (Recon, Exploiter, Reporter) within an isolated Docker environment.
- **🔐 Secure Settings Management**: Encrypted storage for API keys and configurations with automatic failover and performance-based routing.

---

## 🚀 **Quick Start**

For detailed setup on Windows, Linux, or Kali, see the **[Installation Guide](INSTALLATION_GUIDE.md)**.

### **Prerequisites**
- **Docker Desktop** (Required for the security sandbox)
- **Python 3.12+**
- **LLM API Key** (OpenAI, Anthropic, or compatible proxy)

### **Installation**
```bash
# Clone the repository
git clone https://github.com/Hafiz380/enhanced-strix.git
cd enhanced-strix

# Set up virtual environment
python -m venv venv
# Windows: .\venv\Scripts\activate | Linux: source venv/bin/activate

# Install with dependencies
pip install -e .
```

### **Run Your First Assessment**
```bash
# Configure your first provider
strix config add --name default --model gpt-4o --key sk-xxxx

# Start scanning a target
strix --target https://example.com
```

---

## 🔧 **Optimization & Advanced Modes**
To maximize efficiency and minimize costs:
```bash
strix -t https://your-target.com -m quick -n
```
- `-m quick`: Targets high-impact vulnerabilities first, saving time and tokens.
- `-n`: Headless mode for CI/CD integration and reduced local resource usage.

### **Token Usage Reporting**
Monitor your efficiency with real-time stats:
```bash
strix stats
```

---

## 📂 **Project Architecture**
- `strix/`: The heartbeat of the agent logic and orchestrator.
- `strix/skills/ecc/`: A massive library of 150+ security-focused skills.
- `strix/config/`: Secure settings and failover management.
- `docs/`: Comprehensive technical documentation.

## 🤝 **Contributing**
Join the mission to build the most advanced AI security tool. Check out our [Contributing Guide](CONTRIBUTING.md) to get started.

## 📄 **License**
Distributed under the [Apache-2.0 License](LICENSE).

---
<div align="center">
  Built with ❤️ by the security community for a safer web.
</div>
