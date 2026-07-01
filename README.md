# MediChat

MediChat is a local medical RAG chatbot. The backend indexes a medical PDF into a Chroma vector database and answers questions with retrieved context through Ollama.

## Project Structure

```text
medichat/
  backend/
    app.py        # FastAPI chat API
    ingest.py     # PDF indexing script
    data/         # Put the source PDF here locally
    vectordb/     # Generated Chroma database, ignored by Git
  frontend/
    index.html
    style.css
    script.js
  requirements.txt
  .gitignore
```

## Requirements

- Python 3.11+
- Ollama installed and running
- Mistral model pulled in Ollama

```powershell
ollama pull mistral
```

## Setup

Create one virtual environment at the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Place your PDF at:

```text
backend/data/Gale Encyclopedia of Medicine Vol. 1 (A-B) (pages 1-400) (pdfresizer.com).pdf
```

Build the vector database:

```powershell
cd backend
python ingest.py
```

Start the API:

```powershell
uvicorn app:app --reload
```

Open `frontend/index.html` in a browser and ask a question.

## Notes

- Only one environment is needed: `.venv` in the project root.
- The Chroma database is generated in `backend/vectordb`.
- Virtual environments, vector databases, PDFs, caches, and secret files are ignored by Git.

## Git

```powershell
git init
git add .
git commit -m "Initial MediChat project"
git branch -M main
git remote add origin <your-repository-url>
git push -u origin main
```
RETRIVAL EVALUATION

Q: What are the symptoms of anemia?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What causes asthma attacks?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What is an abscess and how does it form?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00






=== Aggregate Manual Retrieval Metrics ===
Mean Precision@3: 0.875
Hit Rate:           0.875