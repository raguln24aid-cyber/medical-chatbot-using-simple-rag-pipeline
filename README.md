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


Q: What are the common treatments for acne?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: How is AIDS transmitted?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What are the effects of chronic alcoholism on the body?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What triggers an allergic reaction?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What are the early signs of Alzheimer's disease?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What is an aneurysm and why is it dangerous?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What causes angina pain?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What are the symptoms of anorexia nervosa?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: How do antibiotics work against bacteria?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What are common symptoms of anxiety disorders?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What are the warning signs of appendicitis?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What is the difference between osteoarthritis and rheumatoid arthritis?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What causes atherosclerosis?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What are the characteristics of autism spectrum disorder?
  Retrieved 0/3 relevant chunks | Precision@3=0.00 | RR=0.00


Q: What are common causes of lower back pain?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What is Bell's palsy and what causes it?
  Retrieved 0/3 relevant chunks | Precision@3=0.00 | RR=0.00


Q: What is a biopsy used for?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What are the mood patterns in bipolar disorder?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What is considered high blood pressure?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: What are the symptoms of bronchitis?
  Retrieved 3/3 relevant chunks | Precision@3=1.00 | RR=1.00


Q: How are burns classified by severity?
  Retrieved 0/3 relevant chunks | Precision@3=0.00 | RR=0.00



=== Aggregate Manual Retrieval Metrics ===
Mean Precision@3: 0.875
Hit Rate:           0.875