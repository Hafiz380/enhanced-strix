# 🦅 Enhanced Strix - Kali Linux Installation Guide

This guide is specifically designed for **Kali Linux** users to set up Enhanced Strix in under 5 minutes.

## 🚀 One-Click Installation (Recommended)

1. Open your terminal in the `enhanced-strix` folder.
2. Give execution permission to the setup script:
   ```bash
   chmod +x setup.sh
   ```
3. Run the automated installer:
   ```bash
   ./setup.sh
   ```

The script will automatically check your system, create a virtual environment, and install all necessary dependencies.

---

## 🛠️ Prerequisites

Before running the installer, ensure you have the following tools:

- **Python 3.12+**: Usually pre-installed on Kali.
- **Docker** (Optional but recommended):
  ```bash
  sudo apt update
  sudo apt install docker.io -y
  sudo usermod -aG docker $USER
  # Log out and log back in for changes to take effect
  ```

---

## 🏃 How to Run Strix on Linux

After successful installation, you can use the `strix-linux.sh` launcher:

### **1. Check Status & Performance**
```bash
./strix-linux.sh stats
```

### **2. Start the Web Interface**
```bash
./strix-linux.sh web
```
Then open `http://localhost:8000` in your browser.

### **3. Start a Target Scan**
```bash
./strix-linux.sh scan -t https://example.com
```

---

## 📁 File Structure for Linux

- **Config File**: `~/.strix/secure-settings.json` (Encrypted)
- **External Config**: `.config/api-config.yaml`
- **Output Runs**: `strix_runs/`

---

## 🛡️ Common Kali Linux Fixes

### **1. Externally-Managed Environment Error**
If you try to run `pip install` directly on Kali, you might see an error. **Do not use `sudo pip`**. Instead, always use the `venv` created by `setup.sh`.

### **2. Docker Permission Denied**
If you see a Docker error, make sure your user is in the `docker` group and you have restarted your session:
```bash
groups # Check if 'docker' is in the list
```

### **3. GUI Issues**
On some Kali installations (XFCE), if the TUI looks broken, ensure your terminal supports Unicode. Running `export LANG=en_US.UTF-8` usually fixes it.

---

## 🧪 Testing on Linux

To verify the installation on Kali:
```bash
source venv/bin/activate
python3 -m pytest tests
```
All tests should pass if dependencies are correctly installed.
