#!/usr/bin/env bash

# 🦅 Enhanced Strix - Automated Setup for Kali Linux
# --------------------------------------------------

set -e # Exit on error

# Visual Header
clear
echo -e "\033[1;34m===============================================\033[0m"
echo -e "\033[1;37;44m   🦅 Enhanced Strix - Automated Setup (Kali) 🦅   \033[0m"
echo -e "\033[1;34m===============================================\033[0m"
echo -e "\033[0;90mPreparing your AI Pentesting environment...\033[0m"
echo ""

# 1. System Checks
echo -e "\033[1;33m[1/5] Checking System Requirements...\033[0m"

# Python Check
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VER=$(python3 --version | awk '{print $2}')
    echo -e "  ✅ Python Found: $PYTHON_VER"
else
    echo -e "  ❌ Python 3 not found! Please run: sudo apt install python3"
    exit 1
fi

# Docker Check
if command -v docker >/dev/null 2>&1; then
    echo -e "  ✅ Docker Found"
else
    echo -e "  ⚠️  Docker not found. Recommended for sandbox features."
    echo -e "     Run: sudo apt install docker.io && sudo usermod -aG docker \$USER"
fi

# 2. Environment Setup
echo ""
echo -e "\033[1;33m[2/5] Creating Virtual Environment (venv)...\033[0m"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "  ✅ venv Created"
else
    echo -e "  ✅ venv Already Exists"
fi

# 3. Dependency Installation
echo ""
echo -e "\033[1;33m[3/5] Installing Required Libraries...\033[0m"
./venv/bin/pip install --upgrade pip > /dev/null
./venv/bin/pip install -e . > /dev/null
echo -e "  ✅ All Libraries Installed"

# 4. Configuration Setup
echo ""
echo -e "\033[1;33m[4/5] Preparing Configuration...\033[0m"
mkdir -p .config
echo -e "  ✅ Configuration Ready"

# 5. Creating Launcher
echo ""
echo -e "\033[1;33m[5/5] Creating Launcher Script...\033[0m"

cat <<EOF > strix-linux.sh
#!/usr/bin/env bash
source "\$(dirname "\$0")/venv/bin/activate"
python3 -m strix.interface.main "\$@"
EOF

chmod +x strix-linux.sh
echo -e "  ✅ Launcher Created (./strix-linux.sh)"

echo ""
echo -e "\033[1;32m===============================================\033[0m"
echo -e "\033[1;37;42m   🎉 INSTALLATION SUCCESSFUL! 🎉   \033[0m"
echo -e "\033[1;32m===============================================\033[0m"
echo ""
echo -e "\033[1;37mNext Steps:\033[0m"
echo -e "\033[0;90m1. Run the tool: \033[1;36m./strix-linux.sh stats\033[0m"
echo -e "\033[0;90m2. Start Web UI: \033[1;36m./strix-linux.sh web\033[0m"
echo ""
echo -e "\033[1;36mHappy Hacking!\033[0m"
echo ""
