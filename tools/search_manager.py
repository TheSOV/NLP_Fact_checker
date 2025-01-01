from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import torch
import os
from pathlib import Path
from typing import Optional

class SearchManager:
    _instance: Optional['SearchManager'] = None
    _vector_store: Optional[FAISS] = None
    _embeddings: Optional[HuggingFaceEmbeddings] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SearchManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._vector_store is None:
            print("Initializing SearchManager...")
            # Dynamically find the project root and set the embeddings path
            project_root = Path(__file__).parent.parent
            embeddings_path = os.path.join(str(project_root), "corpus", "embeddings", "unified_index")
            
            if not os.path.exists(embeddings_path):
                raise ValueError("Unified embeddings not found. Please run create_embeddings.py first.")
                
            self._embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu'}
            )
            self._vector_store = FAISS.load_local(
                embeddings_path, 
                self._embeddings, 
                allow_dangerous_deserialization=True
            )
            print(f"Loaded unified embeddings from {os.path.basename(embeddings_path)}")
    
    @property
    def vector_store(self) -> FAISS:
        return self._vector_store
    
    @property
    def embeddings(self) -> HuggingFaceEmbeddings:
        return self._embeddings
