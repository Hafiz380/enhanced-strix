<p align="center">
  <a href="https://strix.ai/">
    <img src="https://github.com/usestrix/.github/raw/main/imgs/cover.png" alt="Strix Banner" width="100%">
  </a>
</p>

<div align="center">

# Enhanced Strix (Strix + Everything-Claude-Code)

### Open-source AI hackers with ECC-powered intelligence, skills, and memory optimization.

<br/>

<a href="INSTALLATION_GUIDE.md"><img src="https://img.shields.io/badge/Guide-Installation-blue?style=for-the-badge&logo=markdown&logoColor=white" alt="Installation Guide"></a>
<a href="https://strix.ai"><img src="https://img.shields.io/badge/Website-strix.ai-f0f0f0?style=for-the-badge&logoColor=000000" alt="Website"></a>
[![](https://dcbadge.limes.pink/api/server/strix-ai)](https://discord.gg/strix-ai)

<a href="https://github.com/Hafiz380/enhanced-strix"><img src="https://img.shields.io/github/stars/Hafiz380/enhanced-strix?style=flat-square" alt="GitHub Stars"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-3b82f6?style=flat-square" alt="License"></a>

</div>

---

## 🌟 Enhanced Features (ECC Integration)

**Enhanced Strix** is a specialized version that merges the core power of Strix with the advanced performance optimization of **Everything-Claude-Code (ECC)**.

- **🚀 150+ Specialized Skills**: Deep research, language-specific patterns (Go, Rust, Java), and advanced security scanning.
- **🎭 48 AI Personas**: Switch roles between `security-reviewer`, `code-architect`, `bug-hunter`, and more.
- **🧠 Memory Persistence**: Advanced context compression using ECC "Strategic Compact" logic to save tokens.
- **🛡️ Better Verification**: Multi-step validation loops to eliminate false positives.

---

## 💻 Windows Installation Guide (Beginner Friendly)

Follow these steps to set up Enhanced Strix on your Windows machine from scratch.

### 1. Minimum System Requirements
- **OS**: Windows 10 or 11 (64-bit)
- **RAM**: 8GB Minimum (16GB Recommended)
- **Disk Space**: 10GB (for Docker images and project files)
- **Internet**: Stable connection for LLM API and Docker pulls.

### 2. Prerequisite Software
Ensure you have these installed. Click the links for official installers:
1. **Python 3.12+**: [Download here](https://www.python.org/downloads/). *Check "Add Python to PATH" during installation.*
2. **Git**: [Download here](https://git-scm.com/download/win).
3. **Docker Desktop**: [Download here](https://www.docker.com/products/docker-desktop/). *Required for the security sandbox.*

### 3. Step-by-Step Setup (PowerShell)
Open **PowerShell** as Administrator and run these commands one by one:

**Step A: Clone the Project**
```powershell
git clone https://github.com/Hafiz380/enhanced-strix.git
cd enhanced-strix
```

**Step B: Create Virtual Environment**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**Step C: Install Dependencies**
```powershell
pip install -e .
```

### 4. Configuration (Environment Variables)
You must set your AI API key. Replace `your-api-key` with your actual key.

```powershell
# Set the model (e.g., GPT-4o)
$env:STRIX_LLM="openai/gpt-4o"

# Set your API Key
$env:LLM_API_KEY="sk-xxxx-your-key-here"

# Optional: If using a local proxy (like iflow.cn or Ollama)
$env:LLM_API_BASE="http://localhost:20128/v1"
```

### 5. Verification Test
To confirm everything is working, run:
```powershell
strix --version
```
If it shows the version number, your installation is successful!

---

## 🐧 Linux / Kali Linux Installation

Linux users (especially Kali) should use a virtual environment to avoid `externally-managed-environment` errors.

```bash
# Update and Install Essentials
sudo apt update && sudo apt install -y python3-venv python3-pip docker.io git

# Clone and Setup
git clone https://github.com/Hafiz380/enhanced-strix.git
cd enhanced-strix
python3 -m venv venv
source venv/bin/activate
pip install -e .

# Run Verification
python3 -m strix.interface.main --version
```

---

## 🚀 Usage & Low-Resource Mode

To run a scan with **minimum resources** (saves RAM and Tokens), use the following command:

```powershell
# Low Resource Command
strix -t https://your-target.com -m quick -n
```

### Flag Explanation:
- `-t / --target`: The website you want to test.
- `-m quick`: Uses the **Quick Scan** mode. It performs fewer, more targeted tests to save time and processing power.
- `-n / --non-interactive`: Runs in **Headless Mode**. This disables the heavy terminal UI, reducing CPU usage significantly.

**Pro Tip**: To save even more resources, set the reasoning effort to medium:
`$env:STRIX_REASONING_EFFORT="medium"`

---

## 🛠️ Common Errors & Solutions

| Error Message | Solution |
| :--- | :--- |
| **DOCKER NOT INSTALLED** | Ensure Docker Desktop is running and shows a green "Running" status. |
| **Invalid API Key** | Double check your `LLM_API_KEY`. If using a proxy, ensure `LLM_API_BASE` is correct. |
| **externally-managed-environment** | (Linux only) Always activate the `venv` before running `pip`. |
| **ModuleNotFoundError** | Run `pip install -e .` again inside your activated virtual environment. |

---

## ☁️ Strix Platform
Try the full-stack platform at **[app.strix.ai](https://app.strix.ai)** for one-click pentests and auto-remediation.

## 📄 License
Licensed under [Apache-2.0](LICENSE).

---
<div align="center">
  Built with ❤️ by the community. Join our <b><a href="https://discord.gg/strix-ai">Discord</a></b> for support!
</div>
