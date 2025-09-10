# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import employees, chat
from .services.data_service import DataService
from .services.embedding_service import EmbeddingService
from .services.rag_service import RAGService
from .config import SETTINGS

app = FastAPI(title="HR Resource Query Chatbot", version="0.1")

# CORS for local Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routers
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])


@app.on_event("startup")
def startup_event():
    # initialize data and models on startup for fast responses
    print("Loading dataset...")
    DataService.load_data(SETTINGS.EMPLOYEE_DATA_PATH)

    print("Loading embedding model (this may take a few seconds)...")
    EmbeddingService.initialize(model_name=SETTINGS.EMBEDDING_MODEL)

    print("Initializing RAG service...")
    RAGService.initialize(
        embedding_service=EmbeddingService.instance(),
        data_service=DataService.instance(),
        top_k=SETTINGS.TOP_K
    )


@app.get("/")
def root():
    return {"message": "HR Resource Query Chatbot API. Visit /docs for API UI."}
