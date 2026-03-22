# 🤖 HR AI Agent: Precision Employee Intelligence

> Turn your HR data into actionable insights with the power of **Agentic AI** and **Vector Search**.

The **HR AI Agent** is a state-of-the-art employee intelligence platform that leverages the **Endee Vector Database** and **Groq (llama-3.3-70b-versatile)** to provide semantic search, attrition risk assessment, and workforce analysis over any employee dataset — all through a sleek, conversational web interface.

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Flask](https://img.shields.io/badge/backend-Flask-lightgrey.svg)
![Endee](https://img.shields.io/badge/vectordb-Endee-blueviolet.svg)
![Groq](https://img.shields.io/badge/llm-Groq%20llama--3.3--70b-orange.svg)

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [How It Works](#-how-it-works)
- [System Architecture](#-system-architecture)
- [How Endee is Used](#-how-endee-vector-database-is-used)
- [Agentic Workflow](#-agentic-workflow)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [Example Queries](#-example-queries)
- [API Reference](#-api-reference)
- [Dataset Compatibility](#-dataset-compatibility)
- [License](#-license)

---

## 🧭 Overview

Traditional HR analytics requires SQL skills, manual filtering, and static dashboards. The **HR AI Agent** replaces all of that with a single question: *just ask*.

Upload any employee CSV dataset. The agent automatically indexes every record into a high-performance vector index using Endee. From that moment, your entire workforce data becomes queryable in plain English — no SQL, no filters, no code.

Ask things like:
- *"Which departments have the highest attrition?"*
- *"Find senior engineers with low satisfaction in R&D"*
- *"Who are the top earners that still chose to leave?"*

The agent autonomously decides which search tools to invoke, retrieves semantically relevant records from Endee's vector index, reasons over the results, and delivers a structured, data-backed answer.

---

## ✨ Key Features

### 🔍 Semantic Workforce Search
Ask questions in natural language. Unlike keyword search or SQL, Endee's vector similarity finds meaning — so *"find disengaged employees"* returns relevant records even if the word "disengaged" never appears in your dataset.

### 📂 Dynamic CSV Ingestion
Drop any employee CSV and the system automatically:
- Detects column structure
- Builds rich text profiles per employee
- Generates 384-dimensional embeddings via `sentence-transformers`
- Indexes everything into Endee in the background while you wait

### ⚠️ Attrition Risk Detection
Proactively identify employees at risk of leaving. The agent cross-references satisfaction scores, tenure, income, and department data to flag patterns that precede attrition.

### 🏢 Departmental Intelligence
Instantly synthesize department-level summaries — compensation distribution, satisfaction trends, team health, churn rates — without writing a single line of analysis code.

### 🤖 True Agentic Reasoning
The AI doesn't just search — it *reasons*. It picks the right tools, makes multiple Endee queries when needed, synthesizes results, and returns narrative analysis with supporting data.

### 💬 Conversational Memory
The agent maintains context across turns. Ask a follow-up like *"now filter those by R&D only"* and it understands what *"those"* refers to.

### 🎨 Premium Dark UI
A glassmorphism-styled dashboard built for HR professionals — clean, fast, and intuitive.

---

## ⚙️ How It Works

The workflow has two phases:

### Phase 1 — Ingestion
```
User uploads CSV
       ↓
Flask saves file → Triggers background thread
       ↓
Each row → converted to natural language text profile
       ↓
sentence-transformers encodes text → 384-dim float vector
       ↓
Endee Python SDK → index.upsert([{id, vector, meta}])
       ↓
All records stored in Endee cosine index
       ↓
UI polls /status → shows "✓ N records indexed"
```

### Phase 2 — Querying
```
User types query in chat
       ↓
Flask /ask → passes query + conversation history to Groq agent
       ↓
Groq (llama-3.3-70b) decides which tool(s) to call
       ↓
Tool encodes query → vector → Endee index.query(vector, top_k)
       ↓
Endee returns top-K similar employee records
       ↓
Agent synthesizes records → returns structured answer
       ↓
Flask returns response → UI renders in chat bubble
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Browser (UI)                       │
│  ┌──────────────┐        ┌────────────────────────┐  │
│  │   Sidebar    │        │      Chat Panel        │  │
│  │ - CSV Upload │        │ - Message History      │  │
│  │ - Status Bar │        │ - Query Input          │  │
│  │ - Stats Card │        │ - Thinking Indicator   │  │
│  │ - Query Tips │        │ - Tool Call Badges     │  │
│  └──────────────┘        └────────────────────────┘  │
└────────────────────────┬────────────────────────────┘
                         │ HTTP
                         ▼
┌─────────────────────────────────────────────────────┐
│                Flask Backend (app.py)                │
│                                                      │
│  POST /upload  →  Save CSV → spawn thread            │
│  GET  /status  →  Return ingestion progress          │
│  POST /ask     →  Query → Agent → Response           │
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
┌──────────────────┐     ┌──────────────────────────┐
│   Groq Agent     │     │   Endee Ingestion         │
│  (agent.py)      │     │   (endee_setup/ingest.py) │
│                  │     │                           │
│  llama-3.3-70b   │     │  sentence-transformers    │
│  Tool use loop   │     │  → 384-dim embeddings     │
│  Conv. history   │     │  → index.upsert()         │
└────────┬─────────┘     └──────────────────────────┘
         │ Tool calls
         ▼
┌──────────────────────────────────────────────────┐
│              agent/tools.py                       │
│                                                   │
│  search_employees()      → generic semantic search│
│  flag_attrition_risk()   → attrition-focused query│
│  summarize_department()  → department retrieval   │
│  find_low_satisfaction() → satisfaction search    │
│  find_high_earners()     → income-focused search  │
└─────────────────────┬────────────────────────────┘
                      │ index.query(vector, top_k)
                      ▼
┌──────────────────────────────────────────────────┐
│           Endee Vector Database                   │
│           (Docker → localhost:8080)               │
│                                                   │
│  Index: hr_index                                  │
│  Dimension: 384                                   │
│  Space: cosine similarity                         │
│  Precision: INT8                                  │
└──────────────────────────────────────────────────┘
```

---

## 🗄️ How Endee Vector Database is Used

Endee is the **core intelligence layer** of this project. Here's exactly how it's integrated:

### 1. Index Creation
When the user uploads a CSV, a dedicated index is created in Endee:

```python
from endee import Endee, Precision

client = Endee()  # connects to http://localhost:8080

client.create_index(
    name="hr_index",
    dimension=384,          # matches all-MiniLM-L6-v2 output
    space_type="cosine",    # cosine similarity for semantic matching
    precision=Precision.INT8
)
```

### 2. Employee Profile Embedding & Upsert
Each CSV row is converted into a structured text profile and embedded:

```python
# Example profile built from a row:
# "Software Engineer in Research & Development department.
#  Attrition: Yes. Income: $5420. Satisfaction: 2/4.
#  Years at company: 3. Age: 29. ID: 412."

vector = model.encode(text_profile).tolist()  # 384-dim float list

index.upsert([{
    "id": str(row_index),
    "vector": vector,
    "meta": {"text": text_profile}
}])
```

### 3. Semantic Query at Runtime
Every agent tool call performs a vector similarity search:

```python
query_vector = model.encode("employees who left Sales").tolist()
results = index.query(vector=query_vector, top_k=5)
# returns: [{"id": "...", "similarity": 0.94, "meta": {"text": "..."}}, ...]
```

### Why Vector Search Over SQL?
| SQL Filter | Endee Vector Search |
|---|---|
| `WHERE Attrition = 'Yes' AND Department = 'Sales'` | `"Sales employees who left"` |
| Requires exact column names | Works with any column structure |
| No semantic understanding | Finds meaning, not just keywords |
| Breaks on messy/varied data | Robust to schema differences |
| Can't answer *"find disengaged employees"* | Handles abstract concepts naturally |

---

## 🤖 Agentic Workflow

The agent runs in a **while loop**, autonomously calling tools until it has sufficient context to answer:

```
User: "Which department has the most attrition risk?"
         ↓
Agent thinks → calls flag_attrition_risk()
         ↓
Endee returns: 8 employee records with Attrition: Yes
         ↓
Agent analyzes → calls summarize_department("Sales")
         ↓
Endee returns: 10 Sales employee profiles
         ↓
Agent synthesizes both results
         ↓
Response: "Sales has the highest attrition risk with 3 out of 8
           flagged employees. Key factors: low satisfaction (avg 1.8/4)
           and below-market compensation ($3,200 avg monthly income)."
```

### Available Tools

| Tool | Endee Query Strategy | Use Case |
|---|---|---|
| `search_employees` | General semantic search | Any freeform query |
| `flag_attrition_risk` | Attrition-focused embedding | Finding employees who left |
| `summarize_department` | Department-name query | Team overviews |
| `find_low_satisfaction` | Dissatisfaction-focused embedding | Engagement issues |
| `find_high_earners` | Income-focused embedding | Compensation insights |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Vector Database** | [Endee](https://endee.io) | High-performance vector storage and similarity search |
| **LLM / Agent** | Groq — llama-3.3-70b-versatile | Sub-second agentic reasoning and tool use |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) | 384-dimensional semantic text encoding |
| **Backend** | Flask + Python 3.9+ | REST API, file handling, background threading |
| **Frontend** | Vanilla HTML5 / CSS3 / JS | Single-file, zero-dependency UI |
| **Dataset** | Any employee CSV | IBM HR Analytics recommended for testing |

---

## 📁 Project Structure

```
hr-ai-agent/
│
├── app.py                     # Flask server — upload, status, ask endpoints
│
├── templates/
│   └── index.html             # Full UI (sidebar + chat, single file)
│
├── agent/
│   ├── __init__.py
│   ├── agent.py               # Groq agentic loop with conversation history
│   └── tools.py               # 5 Endee-powered semantic search tools
│
├── endee_setup/
│   ├── __init__.py
│   └── ingest.py              # CSV → text profiles → embeddings → Endee upsert
│
├── uploads/                   # Temporary storage for uploaded CSVs
│
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variable template
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Docker (for running Endee server)
- A [Groq API Key](https://console.groq.com) (free)
- Git

### Step 1 — Clone the Repository

```bash
git clone https://github.com/roysa/endeeproject-master.git
cd endeeproject-master
```

### Step 2 — Star & Fork Endee (Mandatory per evaluation criteria)

1. Go to [https://github.com/endee-io/endee](https://github.com/endee-io/endee)
2. Click ⭐ **Star**
3. Click **Fork** → fork to your GitHub account

### Step 3 — Start the Endee Vector Database Server

The Endee Python SDK connects to a locally running Endee server. Start it via Docker:

```bash
# Recommended: Docker Compose
mkdir endee-server && cd endee-server

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
services:
  endee:
    image: endeeio/endee-server:latest
    container_name: endee-server
    ports:
      - "8080:8080"
    environment:
      NDD_NUM_THREADS: 0
      NDD_AUTH_TOKEN: ""
    volumes:
      - endee-data:/data
    restart: unless-stopped
volumes:
  endee-data:
EOF

docker compose up -d
```

Verify it's running:
```bash
curl http://localhost:8080/api/v1/index/list
# Expected: {"indexes": []}
```

### Step 4 — Install Python Dependencies

```bash
cd ..  # back to project root
pip install -r requirements.txt
```

### Step 5 — Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at [console.groq.com](https://console.groq.com).

### Step 6 — Run the App

**Windows:**
```powershell
./start_endee.ps1
```

**Linux / macOS:**
```bash
./run.sh
# or directly:
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## ⚙️ Configuration

| Variable | Description | Default |
|---|---|---|
| `GROQ_API_KEY` | Your Groq API key (required) | — |
| `ENDEE_URL` | Endee server base URL | `http://localhost:8080` |

The Endee Python SDK connects to `localhost:8080` by default. If you run Endee on a different port, update `ingest.py` and `tools.py`:

```python
client = Endee()
client.set_base_url("http://localhost:YOUR_PORT/api/v1")
```

---

## 📖 Usage Guide

### 1. Upload Your Dataset
- Click **Select File** or drag and drop any `.csv` file onto the upload zone
- Recommended: [IBM HR Analytics Dataset](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) from Kaggle
- Any employee CSV works — the agent auto-detects column structure

### 2. Wait for Ingestion
- A progress bar shows ingestion status
- The agent reads "Indexing into Endee..." → "✓ 1,470 records indexed"
- This typically takes 30–60 seconds for ~1,500 records

### 3. Start Querying
- Type any question about your workforce in the chat input
- Press **Enter** to send (Shift+Enter for new line)
- Or click any suggestion chip to auto-fill and submit

### 4. Interpret Results
- AI responses may include narrative analysis, employee lists, or comparison tables
- The tool badge in each AI bubble shows which Endee search was performed
- Ask follow-up questions to drill deeper — the agent remembers context

---

## 💡 Example Queries

### Attrition & Churn
```
Which department has the highest employee churn?
Show me all employees who left the company
Find Sales employees who left
Which job roles have the most attrition?
```

### Satisfaction & Engagement
```
Find employees with low job satisfaction
Who are the most disengaged employees in the company?
Which department has the lowest overall satisfaction?
Find employees with low satisfaction who also left
```

### Compensation
```
Who are the top 5 highest earning employees?
Find the lowest paid employees in the company
Show me high earners who still left the company
Are there any Sales managers earning below average?
```

### Department Insights
```
Give me a summary of the HR department
How many people work in Research and Development?
Which department has the oldest employees?
```

### Analytical & Strategic
```
What patterns do you see among employees who left?
Which role seems most at risk of attrition right now?
Summarize the overall health of the workforce
What should HR focus on to reduce churn?
Give me a risk report for the Sales department
```

---

## 🔌 API Reference

### `POST /upload`
Upload a CSV employee dataset.

**Request:** `multipart/form-data` with field `file` (CSV)

**Response:**
```json
{ "message": "Upload successful, ingestion started." }
```

---

### `GET /status`
Poll the ingestion progress.

**Response (in progress):**
```json
{ "done": false, "error": null, "records": 0 }
```

**Response (complete):**
```json
{ "done": true, "error": null, "records": 1470 }
```

---

### `POST /ask`
Send a query to the HR AI Agent.

**Request:**
```json
{
  "query": "Which Sales employees left the company?",
  "history": [
    { "user": "Hello", "assistant": "Hi! How can I help?" }
  ]
}
```

**Response:**
```json
{
  "answer": "Based on the Endee vector search results, 3 Sales employees left..."
}
```

---

## 📊 Dataset Compatibility

The agent is designed to work with **any employee CSV**. It auto-detects common HR columns and builds smart text profiles. Recommended columns for best results:

| Column | Description |
|---|---|
| `EmployeeNumber` | Unique employee ID |
| `JobRole` | Role/designation |
| `Department` | Team or department name |
| `Attrition` | Yes/No — whether employee left |
| `MonthlyIncome` | Salary data |
| `JobSatisfaction` | Score 1–4 |
| `YearsAtCompany` | Tenure |
| `Age` | Employee age |

If these columns are absent, the agent falls back to encoding all columns as key-value pairs — ensuring compatibility with any CSV structure.

**Recommended test dataset:** [IBM HR Analytics Employee Attrition Dataset](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) — 1,470 employee records, 35 columns.

---

## 📄 License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for full terms.

---

## 🙌 Acknowledgements

- [Endee](https://endee.io) — High-performance open source vector database
- [Groq](https://groq.com) — Ultra-fast LLM inference
- [sentence-transformers](https://www.sbert.net/) — Semantic embedding models
- [IBM HR Analytics Dataset](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) — Kaggle

---

*Made with ❤️ by **Sanchay Roy** (12216677) — LPU*
