

# 🤖 HR AI Agent: Precision Employee Intelligence

> **Turn your HR data into actionable insights with the power of Agentic AI and Vector Search.**

The **HR AI Agent** is a state-of-the-art employee intelligence platform that leverages **Endee Vector Database** and **Llama 3.1 (Groq)** to provide semantic search, attrition risk assessment, and sentiment analysis over workforce datasets.

[![License](https://img.shields.io/badge/license-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/python-3.9+-yellow.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
[![Endee](https://img.shields.io/badge/Vector_DB-Endee-6366f1.svg)](https://endee.io)

---

## ✨ Key Features

*   **🔍 Semantic Workforce Search**: Ask questions in natural language like *"Who are the senior engineers with high performance but low satisfaction?"*
*   **📊 Dynamic Data Ingestion**: Simply drop a CSV file to index your entire employee database into a high-performance vector index.
*   **⚠️ Attrition Risk Detection**: Proactively identify employees at risk of leaving based on satisfaction, tenure, and engagement metrics.
*   **🏢 Departmental Synthesis**: Get instant summaries of department performance, compensation distribution, and team health.
*   **💎 Premium Glassmorphism UI**: A stunning, data-dense dashboard designed for modern HR professionals.

---

## 📸 visual Tour

### 🖥️ The Intelligence Dashboard
A clean, dark-themed interface designed for focus and productivity.
<p align="center">
  <img src="C:\Users\roysa\.gemini\antigravity\brain\444153c7-40d0-4bc8-87ab-f7b59dab24a3\main_dashboard_1773569388191.png" width="90%" style="border-radius: 10px; border: 1px solid #30363d;">
</p>

### 💡 Insight Generation
The AI Agent synthesizes complex queries into easy-to-read tables and narrative analysis.
<p align="center">
  <img src="C:\Users\roysa\.gemini\antigravity\brain\444153c7-40d0-4bc8-87ab-f7b59dab24a3\query_results_1773569452399.png" width="45%" style="border-radius: 10px; border: 1px solid #30363d; margin-right: 5px;">
  <img src="C:\Users\roysa\.gemini\antigravity\brain\444153c7-40d0-4bc8-87ab-f7b59dab24a3\unhappy_employees_results_1773569475073.png" width="45%" style="border-radius: 10px; border: 1px solid #30363d;">
</p>

---

## 🚀 Getting Started

### 1. Prerequisites
*   Python 3.9+
*   [Groq API Key](https://console.groq.com/)
*   [Endee Vector Database](https://github.com/endee-io/endee) (Running via Docker or local build)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/roysa/endeeproject-master.git
cd endeeproject-master

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
ENDEE_URL=http://localhost:8080
```

### 4. Launch
```bash
# The easiest way to start is using the provided script
./start_endee.ps1  # Windows
./run.sh           # Linux/MacOS

# Or run the Flask app directly
python app.py
```
Open `http://localhost:5000` in your browser.

---

## 🛠️ Technical Architecture

The project is built on a robust stack optimized for speed and intelligence:

-   **Frontend**: Vanilla HTML5/CSS3 with a custom Glassmorphism design system.
-   **Backend**: Flask-based REST API for orchestration.
-   **Agentic Layer**: **Llama 3.1-8b** via Groq for sub-second reasoning and tool use.
-   **Knowledge Retrieval**: **Endee Vector Database** for low-latency similarity search.
-   **Embeddings**: `all-MiniLM-L6-v2` for 384-dimensional semantic mapping.

---

## 📄 License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with ❤️ by Sanchay Roy (12216677)
</p>
