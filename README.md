🧠 AI-Powered Inventory Agent System

A hybrid AI system combining LLM-based tool calling, vector search (Qdrant), and multimodal understanding for intelligent stock management.

🚀 Overview

This project is an AI-driven inventory management system that behaves like an autonomous agent.

Instead of traditional CRUD-only logic, the system:

Understands natural language queries 🤖
Decides which tool to execute (search / delete)
Performs semantic search using embeddings 🔎
Enhances retrieval using reranking models 🔁
Supports image understanding via captioning 🖼️

⚙️ System Architecture

(Image placeholder — your mermaid image path should be fixed like this:)

static/images/mermaid-diagram.png
🧠 Key Features
🤖 AI Agent (Gemini)
Converts natural language into structured tool calls
Supports:
search_stock
delete_stock
Automatic argument extraction

🔎 Semantic Search Engine
SentenceTransformer (MiniLM-L6-v2)
Qdrant vector database
Hybrid search:
Semantic similarity
Metadata filtering

🔁 Re-ranking Layer
Cross-Encoder (ms-marco-MiniLM)
Improves relevance scoring
Reorders search results

🖼️ Multimodal AI
BLIP image captioning
Image → Text → Embedding pipeline

📦 Stock Management System
Add / Delete / View items
JSON storage
Sync with vector DB

🌐 Web Interface (Flask)
Add stock items
View inventory
AI query interface
Image upload support

🧱 Tech Stack

Python • Flask • Gemini API • Qdrant • SentenceTransformers • HuggingFace • BLIP • Cross-Encoder • JSON

🧠 AI Pipeline

Image → Caption → Embedding → Vector DB → Query → Rerank → Results


🧩 Tools

🔎 search_stock

Semantic search

Filters:
price
source
product code

❌ delete_stock

Remove item by code

Sync JSON + vector DB


📂 Project Structure


project/
│
├── main.py
├── ai/
│   ├── gemini.py
│   ├── pipeline.py
│   ├── embedding.py
│   ├── qdrant.py
│   ├── reranker.py
│
├── tools/
│   ├── stock_tools.py
│   ├── router.py
│
├── templates/
│   ├── Home.html
│   ├── stock.html
│
├── static/
│   └── UPLOADS/
│
├── Stock.json
└── .env


⚠️ Limitations

No authentication
Basic error handling
Slow startup (model loading)
No logging system

🚀 Future Improvements

JWT authentication
PostgreSQL migration
Docker support
Async pipeline
Embedding cache
Cloud deployment


💡 Why This Project Matters

This project demonstrates a production-style AI architecture:

LLM agent reasoning (Gemini)
Vector database search (Qdrant)
Multimodal AI (BLIP)
Reranking models
Full-stack Flask integration


🏁 Summary

A real AI-powered autonomous inventory system combining:

🧠 LLMs + 🔎 Vector Search + 🖼️ Multimodal AI + ⚙️ Backend Engineering
