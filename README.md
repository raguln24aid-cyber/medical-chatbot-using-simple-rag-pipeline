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
DEMO SCREEN SHORTS:
<img width="1918" height="915" alt="Screenshot 2026-06-19 094123" src="https://github.com/user-attachments/assets/24dcd693-4aa5-4909-9ae7-7d6627697c79" />
<img width="1918" height="917" alt="Screenshot 2026-06-19 094147" src="https://github.com/user-attachments/assets/345f2bf1-9b89-4d17-ae89-2f4ead966366" />
<img width="1915" height="913" alt="Screenshot 2026-06-19 094303" src="https://github.com/user-attachments/assets/8cd07cc4-1cc2-43e0-a4ee-6fad7522eddd" />


