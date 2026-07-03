# 🧠 AI-Powered Inventory Agent System

A hybrid AI system combining LLM-based tool calling, vector search (Qdrant), and multimodal understanding for intelligent stock management.

---

## 🚀 Overview

This project is an AI-driven inventory management system that behaves like an autonomous agent.

Instead of traditional CRUD-only logic, the system:

- Understands natural language queries 🤖  
- Automatically selects tools (search / delete)  
- Performs semantic search using embeddings 🔎  
- Uses reranking for better results 🔁  
- Supports image understanding via captioning 🖼️  

---

## ⚙️ System Architecture

User Input (Natural Language and Image)
        ↓
🤖 LLM Agent (Gemini)
        ↓
Tool Router (Decides Action)
   ├── search_stock
   ├── delete_stock
   └── add_stock (optional extension)
        ↓
🧠 AI Processing Layer
   ├── Image Captioning (BLIP)
   ├── Text Embedding (SentenceTransformers)
        ↓
🔎 Vector Search Engine (Qdrant)
        ↓
🔁 Re-ranking Layer (Cross-Encoder)
        ↓
📦 Structured Results (Stock Items)
        ↓
🌐 Flask Web Interface / API Response


---

## 🧠 Key Features

### 🤖 AI Agent (Gemini)
- Converts natural language into tool calls
- Supports:
  - `search_stock`
  - `delete_stock`
- Auto argument extraction

---

### 🧠 AI Agent Decision Layer
The system uses an LLM (Gemini) as a reasoning engine that:

- Interprets user intent in natural language
- Decides which tool should be executed
- Extracts required parameters automatically
- Routes execution dynamically at runtime

This turns the system from a traditional CRUD application into an **autonomous AI agent system**.

---

### 🔎 Semantic Search Engine
- SentenceTransformer (MiniLM-L6-v2)
- Qdrant vector database
- Hybrid search (semantic + metadata filters)

---

### 🔁 Re-ranking Layer
- Cross-Encoder (ms-marco-MiniLM)
- Improves relevance ranking

---

### 🖼️ Multimodal AI
- BLIP image captioning
- Image → Text → Embedding pipeline

---

### 📦 Stock Management
- Add / Delete / View items
- JSON storage + Qdrant sync

---

### 🌐 Web Interface (Flask)
- Add stock items
- View inventory
- AI query interface
- Image upload support

---

## 🧱 Tech Stack

Python • Flask • Gemini API • Qdrant • SentenceTransformers • HuggingFace • BLIP • Cross-Encoder • JSON

---

## 📂 Project Structure

project/
│
├── main.py
├── ai/
│ ├── gemini.py
│ ├── pipeline.py
│ ├── embedding.py
│ ├── qdrant.py
│ ├── reranker.py
│
├── tools/
│ ├── stock_tools.py
│ ├── router.py
│
├── templates/
│ ├── Home.html
│ ├── stock.html
│
├── static/
│ └── images/
│
├── Stock.json
├── requirements.txt
└── .env



---

## 📦 Installation

1. Clone repo 

   git clone https://github.com/youssefelsayed97/AI-Powered-Inventory-Agent-System.git
  
   cd AI-Powered-Inventory-Agent-System
  
2. Create virtual environment

   python -m venv venv

   Windows:

    venv\Scripts\activate

   Mac/Linux:

    source venv/bin/activate

3. Install dependencies

   pip install -r requirements.txt

   Flask>=3.0.0,<4.0.0
   Werkzeug>=3.0.0,<4.0.0
   python-dotenv>=1.0.0,<2.0.0
   Pillow>=10.0.0,<12.5.0
   qdrant-client>=1.10.0,<2.0.0
   protobuf>=4.25.0,<6.0.0
   sentence-transformers>=2.2.0,<4.0.0
   transformers>=4.35.0,<5.0.0
   torch>=2.0.0,<3.0.0
   numpy>=1.24.0,<2.0.0

🐳 Run Qdrant with Docker

1. Pull image
  docker pull qdrant/qdrant
2. Run container
   docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
3. Verify
  Open in browser:
  http://localhost:6333

  🚀 Run the project
    python main.py

  Then open:
  http://127.0.0.1:5000

⚠️ Limitations
  
  .No authentication
  .Basic error handling
  .Model loading slow at startup
  .No logging system

🚀 Future Improvements

  .JWT authentication
  .PostgreSQL migration
  .Docker full stack setup
  .Async AI pipeline
  .Embedding cache
  .Cloud deployment

💡 Why This Project Matters

  This project demonstrates a production-style AI architecture:

  .🧠 LLM reasoning (Gemini)
  .🔎 Vector search (Qdrant)
  .🖼️ Multimodal AI (BLIP)
  .⚙️ Full-stack Flask system

