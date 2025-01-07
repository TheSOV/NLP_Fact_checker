# Embeddings Utility: Singleton Embedding Management
# Creates a single, reusable HuggingFace embeddings instance
# Automatically detects and uses CUDA if available
# Provides a consistent embedding model across the application

from langchain_huggingface import HuggingFaceEmbeddings
import torch

class Embeddings:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Embeddings, cls).__new__(cls)
            cls._instance._embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu'}
            )
        return cls._instance

embeddings = Embeddings()._embeddings
