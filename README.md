# ⚖️ LexAI — Legal Contract Risk Analyzer

> **AI-powered contract analysis using Cohere Embed v3 + Command R+ with RAG Pipeline**

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)](https://python.org)
[![Cohere](https://img.shields.io/badge/Cohere-Embed%20v3-orange?style=flat-square)](https://cohere.com)
[![LangChain](https://img.shields.io/badge/LangChain-RAG-green?style=flat-square)](https://langchain.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Demo-red?style=flat-square)](https://streamlit.io)

---

## 🎯 What Problem Does This Solve?

Law firms charge **$500+ per hour** to review contracts.

Startups and individuals sign contracts without understanding the risks.

**LexAI analyzes any contract in 30 seconds — for free.**

---

## 🚀 Live Demo

👉 **[Launch App](https://your-app-link.streamlit.app)**

---

## ✨ Features

- 📄 **Upload any PDF contract** — Employment, SaaS, Freelance, Legal agreements
- 🔍 **RAG Pipeline** — Retrieves only relevant clauses using semantic search
- ⚠️ **6 Risk Categories** — Liability, Termination, IP Ownership, Payment, Non-Compete, Indemnification
- 🎯 **Risk Scoring** — HIGH / MEDIUM / LOW classification for each clause
- 📊 **Health Dashboard** — Visual contract health score with gauge + bar chart
- 💬 **Plain English** — Explains legal jargon in simple language
- ⚡ **30 Second Analysis** — Full contract reviewed in under a minute

---

## 🏗️ Architecture

```
PDF Upload
    ↓
PyMuPDF — Extract raw text
    ↓
LangChain TextSplitter — Split into chunks (500 chars)
    ↓
Cohere Embed v3 — Convert chunks to vectors
    ↓
ChromaDB — Store & retrieve vectors
    ↓
RAG — Retrieve top relevant chunks per risk category
    ↓
Cohere Command R+ — Analyze risk level & explain
    ↓
Streamlit — Display visual risk report
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Cohere Command R+ |
| **Embeddings** | Cohere Embed v3 |
| **Vector Database** | ChromaDB |
| **RAG Framework** | LangChain |
| **PDF Parsing** | PyMuPDF (fitz) |
| **Frontend** | Streamlit |
| **Deployment** | Streamlit Cloud |

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/nirmitbhardwaj2510/legal-contract-analyzer.git
cd legal-contract-analyzer

# Create virtual environment
python -m venv myenv
myenv\Scripts\activate  # Windows
source myenv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## ⚙️ Configuration

Create a `.env` file in the root directory:

```env
COHERE_API_KEY=your_cohere_api_key_here
```

Get your free API key at [cohere.com](https://cohere.com)

---

## ▶️ Run Locally

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 📊 Risk Categories Analyzed

| Category | What It Checks |
|---|---|
| **Liability & Damages** | Financial exposure and damage caps |
| **Termination Conditions** | How and when contract can be ended |
| **IP Ownership** | Who owns work created during contract |
| **Payment Terms** | Late fees, penalties, payment schedules |
| **Non-Compete & Confidentiality** | Restrictions after contract ends |
| **Indemnification** | Who covers legal costs if things go wrong |

---

## 🗂️ Project Structure

```
legal-contract-analyzer/
├── app.py              # Streamlit frontend + dashboard
├── analyzer.py         # Core risk analysis logic
├── vector_store.py     # ChromaDB + Cohere embeddings
├── pdf_loader.py       # PDF parsing + chunking
├── requirements.txt    # Dependencies
├── .env                # API keys (not committed)
└── README.md
```

---

## 👨‍💻 Built By

**Nirmit Bhardwaj**
3rd Year B.Tech IT Student — SKIT College, Jaipur

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat-square&logo=linkedin)](https://linkedin.com/in/nirmit-bhardwaj)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=flat-square&logo=github)](https://github.com/nirmitbhardwaj2510)

---

## 📄 License

MIT License — feel free to use and modify.