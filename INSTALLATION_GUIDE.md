# Enhanced Strix: Complete Installation & Setup Guide

This guide provides a step-by-step procedure to install **Enhanced Strix** (integrated with Everything-Claude-Code) on Windows, Linux, and Ubuntu.

---

## **1. Prerequisites**

Before starting the installation, ensure you have the following on your system:

- **Python 3.12 or newer**: Download from [python.org](https://www.python.org/).
- **Docker**: Required for running the security sandbox.
- **Git**: For downloading the code.
- **LLM API Key**: (OpenAI, Anthropic, or a local proxy).

---

## **2. Installation on Windows**

We will use **PowerShell** on Windows.

### **Step 1: Docker Setup**
1. Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Restart your computer after installation.
3. Run Docker Desktop and ensure the green icon in the bottom-left corner says "Running".

### **Step 2: Download Code & Create Environment**
Open **PowerShell** and run these commands:
```powershell
# Clone the repository
git clone https://github.com/Hafiz380/enhanced-strix.git
cd enhanced-strix

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install libraries
pip install -e .
```

### **Step 3: Run the Tool**
```powershell
# Set API Keys
$env:STRIX_LLM="openai/gpt-4o"  # Or your preferred model
$env:LLM_API_KEY="your-api-key"

# Start the scan
strix --target https://example.com

# If 'strix' command doesn't work directly, use:
python -m strix.interface.main --target https://example.com
```

---

## **3. Installation on Linux and Kali Linux**

On Kali Linux, installing Python packages directly is restricted (**externally-managed-environment**), so a virtual environment (venv) is mandatory.

### **Step 1: Install Required Tools**
```bash
sudo apt update
sudo apt install python3-venv python3-pip docker.io git -y

# To run Docker without sudo
sudo usermod -aG docker $USER
# Log out and log back in for changes to take effect
```

### **Step 2: Installation (Specific for Kali Linux)**
```bash
git clone https://github.com/Hafiz380/enhanced-strix.git
cd enhanced-strix

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .
```

### **Step 3: Run the Tool**
```bash
# Set API Keys
export STRIX_LLM="openai/gpt-4o"
export LLM_API_KEY="your-api-key"

# Start the scan
strix --target https://example.com

# If 'strix' command is not found, use:
python3 -m strix.interface.main --target https://example.com
```

---

## **4. Local AI and Proxy Setup**

If you want to use a local model or a proxy server (like `iflow.cn` or `Ollama`):

```powershell
# For Windows
$env:STRIX_LLM="openai/your-model-name"
$env:LLM_API_KEY="your-key"
$env:LLM_API_BASE="http://localhost:20128/v1"

# For Linux
export STRIX_LLM="openai/your-model-name"
export LLM_API_KEY="your-key"
export LLM_API_BASE="http://localhost:20128/v1"
```

---

## **5. Verification**

Perform these checks after installation:
1. **Version Check**: Run `strix --version` to see the version number.
2. **Docker Check**: Run `docker ps` to see an empty list (indicating Docker is running).
3. **ECC Skills Check**: Use `load_skill` within the tool; if it loads skills from the `ecc/` folder, the integration is correct.

---

## **6. Common Issues & Solutions (Troubleshooting)**

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| **externally-managed-environment** | Direct installation on Kali Linux | Always activate `venv` before using `pip`. |
| **neither 'setup.py' nor 'pyproject.toml' found** | Being in the wrong folder | Ensure you are inside the `enhanced-strix` folder (where `pyproject.toml` is). |
| **DOCKER NOT INSTALLED** | Docker is not running | Run Docker Desktop or `sudo systemctl start docker`. |
| **ModuleNotFoundError** | Libraries not installed | Run `pip install -e .` again (inside venv). |

---

**Note**: This tool pulls a Docker image on the first run, which may take 5-10 minutes. Please be patient!
