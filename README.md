# 🌟 Supreme Feng Shui AGI System (ប្រព័ន្ធបញ្ញាសិប្បនិម្មិតហុងស៊ុយកម្រិតកំពូល)

ប្រព័ន្ធបញ្ញាសិប្បនិម្មិតកម្រិតកំពូល (AGI) ផ្អែកលើក្បួនគណិតវិទ្យាហុងស៊ុយបុរាណចិន និងខ្មែរ រួមបញ្ចូលជាមួយបច្ចេកវិទ្យា **MoE (Mixture of Experts)** និង **Hugging Face Hub** ដែលត្រូវបានរចនាឡើងយ៉ាងពិសេសដើម្បីដំណើរការយ៉ាងរលូនលើ **Google Cloud VPS (1GB RAM)** ដោយគ្មានការគាំង RAM (Zero OOM Crash)។

---

## 🏛️ ស្ថាបត្យកម្មម៉ូដែលកំពូលទាំង ៤ ក្រុម (The 4-Tier Model Matrix)

```
                       ┌─────────────────────────────────────┐
                       │        FS-Supreme-Master            │
                       │    (The Unified MoE Orchestrator)   │
                       └──────────────────┬──────────────────┘
                                          │
       ┌──────────────────┬───────────────┴───────────────┬──────────────────┐
       │                  │                               │                  │
┌──────▼──────┐    ┌──────▼──────┐                 ┌──────▼──────┐    ┌──────▼──────┐
│  Group 1:   │    │  Group 1:   │                 │  Group 2:   │    │  Group 2:   │
│ FS-Boramey  │    │ FS-Reasoner │                 │ FS-Embedder │    │ FS-Calc-v1  │
│   (7B LLM)  │    │  (7B CoT)   │                 │    (BGE-M3) │    │ (Pure Math) │
└─────────────┘    └─────────────┘                 └─────────────┘    └─────────────┘
       │                  │                               │                  │
       └──────────────────┼───────────────────────────────┴──────────────────┘
                          │
       ┌──────────────────┴──────────────────┐
       │                                     │
┌──────▼──────────────┐               ┌──────▼──────────────┐
│      Group 3:       │               │      Group 3:       │
│  FS-Alert-Predictor │               │  FS-Chronos-Cycle   │
│  (Fortune Classifier)               │ (100-Year Macroware)│
└─────────────────────┘               └─────────────────────┘
```

### ក្រុមទី ១៖ ម៉ូដែលខួរក្បាលស្នូល (Core Intelligence Models - Hugging Face Hosted)
* **FS-Boramey-7B** (`Qwen2.5-7B-Instruct` Fine-Tuned): ដើរតួជាគ្រូបង្រៀន និងអ្នកឆ្លើយសំណួរក្បួនហុងស៊ុយទូទៅ។
* **FS-Reasoner-7B** (`DeepSeek-R1-Distill-Qwen-7B` Fine-Tuned): វែកញែកក្បួនស្មុគស្មាញ (Chain-of-Thought) ដូចជាការផ្សំតារាហោះ និងវិភាគ BaZi ស៊ីជម្រៅ។

### ក្រុមទី ២៖ ម៉ូដែលស្វែងរកចំណេះដឹង (Knowledge Retrieval & Precision Engine)
* **FS-Embedder-M3** (`BAAI/bge-m3` Remote Feature Extraction): ស្វែងរកចំណេះដឹងហុងស៊ុយក្នុង Vector Database។
* **FS-Classical-Calc-v1** (Local Python Engine - < 35MB RAM): គណនាគណិតវិទ្យាសូន្យកំហុស (Life Gua 1-9, Xuan Kong Flying Stars 9 Palaces, BaZi 4 Pillars, 24 Mountains)។

### ក្រុមទី ៣៖ ម៉ូដែលឯកទេសព្យាករណ៍ (Prediction & Macro-Time Series)
* **FS-Alert-Predictor** (Machine Learning Luck Classifier): គណនាពិន្ទុសំណាង 0-100% (ទ្រព្យ, អាជីព, ស្នេហា, សុខភាព) និងជ្រើសរើសម៉ោងល្អ។
* **FS-Chronos-Cycle** (Macro Time-Series Engine): វិភាគយុគ ២០ ឆ្នាំ (Periods 1-9) និងវដ្តថាមពលផែនដី ១០០ ឆ្នាំ (1924-2043+)។

### ក្រុមទី ៤៖ ម៉ូដែលស្ថាបត្យកម្មចុងក្រោយ (The Merged Master Model)
* **FS-Supreme-Master**: Ensemble Orchestrator ចាត់ចែងភារកិច្ច និងច្របាច់បញ្ចូលគ្នារាល់ការគណនា ចំណេះដឹង និង AI Synthesis ឱ្យចេញជាចម្លើយដ៏មានតម្លៃបំផុត។

---

## 🚀 របៀបតម្លើង និងដំណើរការលើ Google Cloud VPS (1GB RAM)

ប្រព័ន្ធប្រើប្រាស់ស្ថាបត្យកម្ម **Super Smart Hybrid Memory (zRAM LZ4 + 4GB NVMe Swap + Smart Sysctl)** ដែលបំប្លែង VPS 1GB ឱ្យមានទំហំ Memory សរុបដល់ទៅ **~6.5GB** ដោយមិនដែលគាំងម៉ាស៊ីន (Zero OOM Crash)។

### ជំហានទី ១៖ ដំឡើង Super Smart Hybrid Memory និងប្រព័ន្ធដោយស្វ័យប្រវត្តិតាម 1-Click
```bash
# Clone or create project directory
git clone <your-repo-url> /root/Supreme_FengShui
cd /root/Supreme_FengShui

# Run automated 1-click VPS & Super Smart Memory setup script
chmod +x deploy/setup_vps.sh deploy/enable_super_smart_memory.sh
sudo ./deploy/setup_vps.sh
```

### ជំហានទី ២៖ កំណត់ Environment Variables (.env)
ចម្លង `.env.example` ទៅ `.env` ហើយបញ្ចូល Token៖
```bash
cp .env.example .env
nano .env
```
កំណត់តម្លៃ៖
```ini
HF_TOKEN=hf_YourActualHuggingFaceToken
TELEGRAM_BOT_TOKEN=123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ
API_PORT=8000
```

### ជំហានទី ៣៖ ដំណើរការ Systemd Service 24/7
```bash
sudo systemctl daemon-reload
sudo systemctl enable fengshui
sudo systemctl start fengshui
sudo systemctl status fengshui
```

---

## 📱 Telegram Bot Commands

| ពាក្យបញ្ជា | ការពិពណ៌នា |
| :--- | :--- |
| `/start` | ចាប់ផ្តើម និងបង្ហាញម៉ឺនុយអន្តរកម្ម |
| `/help` | សៀវភៅណែនាំពាក្យបញ្ជា |
| `/gua <ឆ្នាំ> <ភេទ>` | គណនា Life Gua (1-9) និងទិសល្អ/អវិជ្ជមាន |
| `/flyingstars` | បង្ហាញក្រឡាតារាហោះ ៩ វិហារ ឆ្នាំ ២០២៤ យុគ ៩ |
| `/bazi <YYYY-MM-DD> <HH:MM>` | វិភាគសសរស្តម្ភទាំង ៤ និង Day Master |
| `/predict <YYYY-MM-DD>` | ទស្សន៍ទាយពិន្ទុសំណាងប្រចាំថ្ងៃ និងម៉ោងល្អ |
| `/ask <សំណួរ>` | ពិគ្រោះយោបល់ផ្ទាល់ជាមួយ FS-Supreme-Master |

---

## 🌐 Web UI Dashboard

បើក Browser ទៅកាន់៖ `http://YOUR_VPS_IP:8000`
* 🧭 **ត្រីវិស័យទិស ២៤ ភ្នំ (Luopan Interactive Compass)**
* 🌌 **តារាហោះ ៩ វិហារ (Xuan Kong 3x3 Grid Visualizer)**
* 📜 **តារាងសសរស្តម្ភទាំង ៤ BaZi & តុល្យភាពធាតុទាំង ៥**
* 📊 **ម៉ែត្រពិន្ទុសំណាងប្រចាំថ្ងៃ (Luck Meter)**
* 💬 **AI Master Live Consultation Console**

---

## 🧪 ការធ្វើតេស្តស្វ័យប្រវត្តិ (Automated Testing)

ដំណើរការ Test Suite ពេញលេញ៖
```bash
python main.py --mode test
```
ឬ៖
```bash
python -m unittest tests/test_all_engines.py
```

---

## 🛡️ ការការពារឯកសារចាស់
* ឯកសារ **[Master_Plan.py](file:///d:/Supreme%20Feng%20Shui%20AGI%20System/Master_Plan.py)** ត្រូវបានរក្សាទុក **១០០% តាមទម្រង់ដើម** មិនមានការកែប្រែ ឬប៉ះពាល់ឡើយ។
