# AI Job Agent for WhatsApp Community

A fully local, modular AI-powered agent that scrapes fresh AI/ML job listings, filters them using a local LLM (via Ollama), and sends the relevant jobs to a WhatsApp group — all triggered via terminal or by a special command message from a group admin.

---

## Tech Stack

| Layer              | Technology                                  |
| ------------------ | ------------------------------------------- |
| Scraping           | `requests`, `BeautifulSoup` (Python)        |
| Filtering          | `Ollama` (local LLM like `mistral`)         |
| Messaging          | `Baileys` (Node.js WhatsApp library)        |
| Trigger System     | `typer` CLI (Python) + Baileys msg listener |
| Environment Config | `.env` + `python-dotenv`                    |

---

## Folder Structure

```
job-agent/
├── config/
│   ├── __init__.py
│   └── settings.py         # Loads env vars like model name, delay, etc.
│
├── data/
│   ├── jobs_raw.json       # Scraped jobs (pre-filter)
│   └── jobs_filtered.json  # Filtered jobs (to be sent)
│
├── filters/
│   ├── __init__.py
│   └── ollama_filter.py    # Sends job list to Ollama for filtering
│
├── messenger/
│   ├── __init__.py
│   ├── agent_listener_baileys.js  # WhatsApp group listener via Baileys
│   └── send_message.js     # (Optional) direct send script for Phase 4
│
├── scrapers/
│   ├── __init__.py
│   └── ai_jobs_scraper.py  # Scrapes jobs from ai-jobs.net
│
├── utils/
│   ├── __init__.py
│   └── logger.py           # Central logger for unified logging
│
├── main.py                 # CLI entrypoint: scrape, filter, message, run
├── requirements.txt        # Python dependencies
├── package.json            # Node.js deps (Baileys etc.)
├── .gitignore              # Ignores node_modules, data files, etc.
├── README.md               # Project documentation
└── test_import.py          # Sanity check for imports across modules

```

---

## How It Works

### 🔹 Phase 1: Core Setup

* Modular folder structure
* CLI entrypoint using `typer`
* Logging and environment config

### 🔹 Phase 2: LLM Filtering

* Uses [Ollama](https://ollama.com/) to filter jobs locally
* Prompts the model to return structured JSON of jobs matching filters (e.g. remote, entry-level, ML)

### 🔹 Phase 3: Web Scraping

* Scrapes `https://ai-jobs.net`
* Extracts job title, company, location, and URL

### 🔹 Phase 4: Messaging to WhatsApp

* Uses `Baileys` to send filtered jobs to a group
* Sends jobs in formatted messages via WhatsApp Web session

### 🔹 Phase 5: Command-Based Trigger System

* Supports two trigger modes:

  * CLI: `python main.py run`
  * WhatsApp: Group admin sends `!jobbot` → pipeline runs and replies in chat

---

## ⚙️ Setup Instructions

### 🔹 1. Clone & Setup Python Env

```bash
git clone https://github.com/yourname/job-agent
cd job-agent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 🔹 2. Setup `.env`

```env
OLLAMA_MODEL=mistral
WHATSAPP_GROUP=Your Group Name
SCRAPER_DELAY=2
```

### 🔹 3. Setup Baileys WhatsApp Agent

```bash
cd messenger
npm init -y
npm install baileys @whiskeysockets/baileys
node send_message.js   # shows QR code on first run
```

Scan the QR using WhatsApp on your phone.

---

## 🔧 CLI Commands

```bash
# Phase-wise
python main.py scrape     # Scrape jobs
python main.py filter     # Filter with Ollama
python main.py message    # Send jobs (if using script-based send)

# Full pipeline
python main.py run        # Scrape → Filter → Send

# WhatsApp Trigger
# Send "!jobbot" in the group as admin
```

---

## Privacy & FOSS Note

* 100% local execution
* No cloud dependencies
* Built using open-source libraries only

---

## Future Enhancements (Optional)

* Multi-source scraping (RemoteOK, Wellfound, Greenhouse)
* Job deduplication using local DB (SQLite/JSON store)
* Telegram parallel agent
* Dashboard UI via Streamlit or Gradio
* Cron-based auto-scheduling
* Voice or audio command triggers

---

