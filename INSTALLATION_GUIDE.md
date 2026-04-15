# Enhanced Strix: مکمل انسٹالیشن اور سیٹ اپ گائیڈ

اس گائیڈ میں **Enhanced Strix** (جس میں Everything-Claude-Code انٹیگریٹڈ ہے) کو ونڈوز، لینکس، اور اوبنٹو پر انسٹال کرنے کا مکمل طریقہ کار بیان کیا گیا ہے۔

---

## **1. بنیادی ضروریات (Prerequisites)**

انسٹالیشن شروع کرنے سے پہلے یقینی بنائیں کہ آپ کے سسٹم میں درج ذیل چیزیں موجود ہیں:

- **Python 3.12 یا اس سے جدید**: [python.org](https://www.python.org/) سے ڈاؤن لوڈ کریں۔
- **Docker**: سیکیورٹی سینڈ باکس چلانے کے لیے لازمی ہے۔
- **Git**: کوڈ ڈاؤن لوڈ کرنے کے لیے۔
- **LLM API Key**: (OpenAI, Anthropic, یا کوئی لوکل پراکسی)۔

---

## **2. ونڈوز (Windows) پر انسٹالیشن**

ونڈوز پر ہم **PowerShell** استعمال کریں گے۔

### **مرحلہ 1: ڈوکر (Docker) کا سیٹ اپ**
1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) ڈاؤن لوڈ اور انسٹال کریں۔
2. انسٹالیشن کے بعد کمپیوٹر ری اسٹارٹ کریں۔
3. ڈوکر ڈیسک ٹاپ چلائیں اور یقینی بنائیں کہ نیچے بائیں کونے میں سبز رنگ کا آئیکون "Running" دکھا رہا ہے۔

### **مرحلہ 2: کوڈ ڈاؤن لوڈ اور انوائرمنٹ بنانا**
ٹرمینل (PowerShell) کھولیں اور یہ کمانڈز چلائیں:
```powershell
# کوڈ کلون کریں
git clone https://github.com/Hafiz380/enhanced-strix.git
cd enhanced-strix

# ورچوئل انوائرمنٹ بنائیں
python -m venv venv
.\venv\Scripts\activate

# لائبریریز انسٹال کریں
pip install -e .
```

### **مرحلہ 3: ٹول چلانا**
```powershell
# API Keys سیٹ کریں
$env:STRIX_LLM="openai/gpt-4o"  # یا اپنا ماڈل
$env:LLM_API_KEY="your-api-key"

# اسکین شروع کریں
strix --target https://example.com

# اگر 'strix' کمانڈ نہ چلے تو یہ استعمال کریں:
python -m strix.interface.main --target https://example.com
```

---

## **3. لینکس اور کالی لینکس (Linux / Kali) پر انسٹالیشن**

کالی لینکس (Kali Linux) پر پائتھن پیکیجز کو براہ راست انسٹال کرنا منع ہے (**externally-managed-environment**)، اس لیے ورچوئل انوائرمنٹ (venv) لازمی ہے۔

### **مرحلہ 1: ضروری ٹولز انسٹال کریں**
```bash
sudo apt update
sudo apt install python3-venv python3-pip docker.io git -y

# ڈوکر کو بغیر sudo کے چلانے کے لیے
sudo usermod -aG docker $USER
# اس کے بعد لاگ آؤٹ کر کے دوبارہ لاگ ان کریں
```

### **مرحلہ 2: انسٹالیشن (کالی لینکس کے لیے مخصوص طریقہ)**
```bash
git clone https://github.com/Hafiz380/enhanced-strix.git
cd enhanced-strix

# ورچوئل انوائرمنٹ بنانا اور ایکٹیویٹ کرنا
python3 -m venv venv
source venv/bin/activate

# اب ڈیپینڈنسیز انسٹال کریں
pip install -e .
```

### **مرحلہ 3: ٹول چلانا**
```bash
# API Keys سیٹ کریں
export STRIX_LLM="openai/gpt-4o"
export LLM_API_KEY="your-api-key"

# اسکین شروع کریں
strix --target https://example.com

# اگر 'strix' کمانڈ نہ ملے تو یہ استعمال کریں (Trae Terminal طریقہ):
python3 -m strix.interface.main --target https://example.com
```

---

## **4. لوکل AI (Local AI) اور پراکسی سیٹ اپ**

اگر آپ اپنا لوکل ماڈل یا پراکسی سرور (جیسے `iflow.cn` یا `Ollama`) استعمال کرنا چاہتے ہیں:

```powershell
# ونڈوز کے لیے
$env:STRIX_LLM="openai/your-model-name"
$env:LLM_API_KEY="your-key"
$env:LLM_API_BASE="http://localhost:20128/v1"

# لینکس کے لیے
export STRIX_LLM="openai/your-model-name"
export LLM_API_KEY="your-key"
export LLM_API_BASE="http://localhost:20128/v1"
```

---

## **5. وریفیکیشن (Verification)**

انسٹالیشن کے بعد یہ چیکس کریں:
1. **Version Check**: `strix --version` چلائیں، یہ ورژن دکھائے گا۔
2. **Docker Check**: `docker ps` چلائیں، یہ خالی لسٹ دکھائے گا (یعنی ڈوکر چل رہا ہے)۔
3. **ECC Skills Check**: ٹول کے اندر `load_skill` استعمال کریں، اگر وہ `ecc/` فولڈر سے اسکلز لوڈ کر رہا ہے تو انٹیگریشن درست ہے۔

---

## **6. عام مسائل اور ان کے حل (Troubleshooting)**

| مسئلہ | وجہ | حل |
| :--- | :--- | :--- |
| **externally-managed-environment** | کالی لینکس پر براہ راست انسٹالیشن | ہمیشہ `venv` ایکٹیویٹ کر کے `pip` استعمال کریں۔ |
| **neither 'setup.py' nor 'pyproject.toml' found** | غلط فولڈر میں ہونا | یقینی بنائیں کہ آپ `enhanced-strix` فولڈر کے اندر ہیں (جہاں `pyproject.toml` ہے)۔ |
| **DOCKER NOT INSTALLED** | ڈوکر نہیں چل رہا | ڈوکر ڈیسک ٹاپ چلائیں یا `sudo systemctl start docker` کریں۔ |
| **ModuleNotFoundError** | لائبریریز انسٹال نہیں ہوئیں | دوبارہ `pip install -e .` چلائیں (venv کے اندر)۔ |

---

**نوٹ**: یہ ٹول پہلی بار چلنے پر ڈوکر امیج ڈاؤن لوڈ کرتا ہے جس میں 5-10 منٹ لگ سکتے ہیں۔ صبر سے کام لیں!
