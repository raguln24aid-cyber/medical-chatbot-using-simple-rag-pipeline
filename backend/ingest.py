from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
VECTOR_DB_DIR = BASE_DIR / "vectordb"
PDF_PATH = DATA_DIR / "Gale Encyclopedia of Medicine Vol. 1 (A-B) (pages 1-400) (pdfresizer.com).pdf"

loader = PyPDFLoader(str(PDF_PATH))
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    chunks,
    embeddings,
    persist_directory=str(VECTOR_DB_DIR)
)

db.persist()

print("PDF indexed successfully")
