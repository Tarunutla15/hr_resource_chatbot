# # backend/app/config.py
from pydantic_settings import BaseSettings
from pathlib import Path

# class Settings(BaseSettings):
#     # Data
#     EMPLOYEE_DATA_PATH: str = str(Path(__file__).resolve().parents[1] / "data" / "employees.json")
#     # Embedding model to use
#     EMBEDDING_MODEL: str = "sentence-transformers/multi-qa-mpnet-base-dot-v1"
#     # RAG behavior
#     TOP_K: int = 3
#     # Ollama (optional) - we call locally by Python package if available
#     OLLAMA_MODEL: str = "mistral"
#     # Server
#     API_HOST: str = "127.0.0.1"
#     API_PORT: int = 8000

#     class Config:
#         env_file = ".env.example"

# SETTINGS = Settings()
# In config.py, add proper environment handling:
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    EMPLOYEE_DATA_PATH: str = str(Path(__file__).resolve().parents[1] / "data" / "employees.json")
    EMBEDDING_MODEL: str = "sentence-transformers/all-mpnet-base-v2"
    TOP_K: int = 3
    USE_OLLAMA: bool = False
    OLLAMA_MODEL: str = "mistral"
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()

SETTINGS = get_settings()