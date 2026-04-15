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
cd enhanced-strix/strix

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
```

---

## **3. لینکس اور اوبنٹو (Linux / Ubuntu) پر انسٹالیشن**

### **مرحلہ 1: ضروری ٹولز انسٹال کریں**
```bash
sudo apt update
sudo apt install python3-venv python3-pip docker.io git -y

# ڈوکر کو بغیر sudo کے چلانے کے لیے (اختیاری لیکن تجویز کردہ)
sudo usermod -aG docker $USER
# اس کے بعد لاگ آؤٹ کر کے دوبارہ لاگ ان کریں
```

### **مرحلہ 2: انسٹالیشن**
```bash
git clone https://github.com/Hafiz380/enhanced-strix.git
cd enhanced-strix/strix

python3 -m venv venv
source venv/bin/activate
pip install -e .
```

---

## **4. لوکل AI (Local AI) اور پراکسی سیٹ اپ**

اگر آپ اپنا لوکل ماڈل یا پراکسی سرور (جیسے `iflow.cn` یا `Ollama`) استعمال کرنا چاہتے ہیں:

```powershell
# ونڈوز کے لیے
$env:STRIX_LLM="openai/your-model-name"
$env:LLM_API_KEY="your-key"
$env:LLM_API_BASE="http://localhost:20128/v1" # اپنا پراکسی URL دیں

# لینکس کے لیے
export STRIX_LLM="openai/your-model-name"
export LLM_API_KEY="your-key"
export LLM_API_BASE="http://localhost:20128/v1"
```

---

## **5. وریفیکیشن (کیسے پتہ چلے کہ سب ٹھیک ہے؟)**

انسٹالیشن کے بعد یہ چیکس کریں:
1. **Version Check**: `strix --version` چلائیں، یہ ورژن دکھائے گا۔
2. **Docker Check**: `docker ps` چلائیں، یہ خالی لسٹ دکھائے گا (یعنی ڈوکر چل رہا ہے)۔
3. **ECC Skills Check**: ٹول کے اندر `load_skill` استعمال کریں، اگر وہ `ecc/` فولڈر سے اسکلز لوڈ کر رہا ہے تو انٹیگریشن درست ہے۔

---

## **6. عام مسائل اور ان کے حل (Troubleshooting)**

| مسئلہ | وجہ | حل |
| :--- | :--- | :--- |
| **DOCKER NOT INSTALLED** | ڈوکر نہیں چل رہا یا انسٹال نہیں ہے | ڈوکر ڈیسک ٹاپ چلائیں یا `sudo systemctl start docker` کریں۔ |
| **ModuleNotFoundError** | لائبریریز انسٹال نہیں ہوئیں | دوبارہ `pip install -e .` چلائیں۔ |
| **Invalid API Key** | غلط Key یا پراکسی مسئلہ | اپنا API Key اور Base URL دوبارہ چیک کریں۔ |
| **Permission Denied** | sudo کی ضرورت ہے | کمانڈ کے شروع میں `sudo` لگائیں یا یوزر پرمیشنز درست کریں۔ |

---

**نوٹ**: یہ ٹول پہلی بار چلنے پر ڈوکر امیج ڈاؤن لوڈ کرتا ہے جس میں 5-10 منٹ لگ سکتے ہیں۔ صبر سے کام لیں!
