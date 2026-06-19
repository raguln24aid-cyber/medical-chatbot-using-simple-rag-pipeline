# 🩺 MediChat – Medical RAG Chatbot

MediChat is a Retrieval-Augmented Generation (RAG) based medical chatbot that answers healthcare-related questions using information retrieved from a medical encyclopedia PDF.

The application combines semantic search, vector embeddings, and a local Large Language Model (LLM) to provide context-aware responses while minimizing hallucinations.

---

## 🚀 Features

* Medical Question Answering using RAG
* Local LLM Inference with Ollama + Mistral
* Semantic Search using Vector Embeddings
* ChromaDB Vector Database
* FastAPI Backend
* Interactive Frontend (HTML, CSS, JavaScript)
* Privacy-Friendly (Runs Locally)
* PDF Knowledge Base Ingestion Pipeline

---

## 🏗️ Architecture

User Question
↓
Embedding Generation
↓
Similarity Search (ChromaDB)
↓
Top-K Relevant Chunks Retrieved
↓
Context Augmentation
↓
Mistral (Ollama)
↓
Final Answer

---

## 🔍 Retrieval Strategy

### Document Processing

The medical encyclopedia PDF is processed using:

* PyPDFLoader for document extraction
* RecursiveCharacterTextSplitter

  * Chunk Size: 500
  * Chunk Overlap: 50

This strategy preserves context while preventing information loss between chunks.

### Embedding Model

Model Used:

sentence-transformers/all-MiniLM-L6-v2

The embedding model converts document chunks and user queries into dense vector representations for semantic retrieval.

### Vector Database

* ChromaDB
* Persistent Local Storage
* Fast Similarity Search

### Retrieval Method

Similarity Search

Configuration:

* Top-K Retrieval = 3

For every user query:

1. Query is converted into embeddings.
2. ChromaDB performs semantic similarity search.
3. Top 3 relevant chunks are retrieved.
4. Retrieved context is injected into the prompt.
5. Mistral generates the final answer using only retrieved information.

This reduces hallucinations and improves factual grounding.

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* LangChain
* ChromaDB
* Ollama
* Mistral

### AI Components

* Retrieval-Augmented Generation (RAG)
* Sentence Transformers
* Vector Embeddings
* Semantic Search

### Frontend

* HTML
* CSS
* JavaScript

---

## 📂 Project Structure

medichat/

├── backend/

│ ├── app.py

│ ├── ingest.py

│ ├── data/

│ └── vectordb/

│

├── frontend/

│ ├── index.html

│ ├── style.css

│ └── script.js

│

├── requirements.txt

├── .gitignore

└── README.md

---

## ⚙️ Installation

### 1. Clone Repository

git clone <repository-url>

cd medichat

### 2. Create Virtual Environment

python -m venv .venv

Windows:

..venv\Scripts\Activate.ps1

### 3. Install Dependencies

pip install -r requirements.txt

---

## 📚 Add Medical Dataset

Place your medical PDF inside:

backend/data/

Example:

Gale Encyclopedia of Medicine Vol. 1 (A-B)

---

## 🧠 Build Vector Database

cd backend

python ingest.py

This will:

* Load PDF
* Split into chunks
* Generate embeddings
* Store vectors in ChromaDB

---

## ▶️ Run Backend

cd backend

uvicorn app:app --reload

API Endpoint:

http://localhost:8000

---

## 💬 Run Frontend

Open:

frontend/index.html

in your browser.

Ask medical questions and receive context-aware responses from the RAG pipeline.

---

## 📸 Demo

### Chat Interface
HOME:
<img width="1918" height="915" alt="Screenshot 2026-06-19 094123" src="https://github.com/user-attachments/assets/fbe40f84-cb0d-407a-a0f2-a77073d0cc44" />

CHAT INTEFACE:
<img width="1918" height="917" alt="Screenshot 2026-06-19 094147" src="https://github.com/user-attachments/assets/5926f5fd-ea35-4886-9d53-ba6c7d0a5826" />

OUTPUT:
<img width="1915" height="913" alt="Screenshot 2026-06-19 094303" src="https://github.com/user-attachments/assets/02fa5aea-d819-419d-880b-10e512131e1d" />





---

## 🔮 Future Improvements

* Hybrid Search (BM25 + Vector Search)
* Conversation Memory
* Source Citations
* Multi-PDF Knowledge Base
* Medical Report Analysis
* Authentication & User History
* Streaming Responses
* Docker Deployment

---

## 👨‍💻 Author

Ragul N

Artificial Intelligence & Data Science Student

Passionate about Generative AI, RAG Systems, Agentic AI, LangGraph, MCP, and FastAPI Development.
