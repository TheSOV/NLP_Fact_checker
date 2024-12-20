from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
from typing import List, Type, Dict, Union

import os
from pathlib import Path
import re
import unicodedata
import json
import torch

class RAGSearchInput(BaseModel):
    """Input schema for RAGSearchTool matching InputAnalysisOutput."""
    original_request: str = Field(..., description="The original request exactly as provided")
    request_in_english: str = Field(..., description="The request translated to English if needed")
    verification_facts: List[str] = Field(..., description="List of facts that need verification")
    possible_questions: List[str] = Field(..., description="List of questions useful for verification")
    original_language: str = Field(..., description="Detected language of the original text")

class RAGSearchTool(BaseTool):
    name: str = "RAG Search Tool"
    description: str = "Search through documents using RAG (Retrieval Augmented Generation) to find relevant information."
    args_schema: Type[BaseModel] = RAGSearchInput
    
    _embeddings_path: str = PrivateAttr()
    _vector_store: FAISS = PrivateAttr()
    
    def __init__(self, **data):
        """Initialize RAG tool with unified FAISS embeddings."""
        super().__init__(**data)
        
        # Dynamically find the project root and set the embeddings path
        project_root = Path(__file__).parent.parent
        self._embeddings_path = os.path.join(str(project_root), "corpus", "embeddings", "unified_index")
        
        if not os.path.exists(self._embeddings_path):
            raise ValueError("Unified embeddings not found. Please run create_embeddings.py first.")
            
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2",
            model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu'}
        )
        self._vector_store = FAISS.load_local(self._embeddings_path, embeddings, allow_dangerous_deserialization=True)
        print(f"Loaded unified embeddings from {os.path.basename(self._embeddings_path)}")
    
    def search(self, query: str, k: int = 5) -> List[Document]:
        """Search for relevant documents."""
        docs = self._vector_store.similarity_search(query, k=k)
        return docs
    
    def _run(self, 
            original_request: str,
            request_in_english: str,
            verification_facts: List[str],
            possible_questions: List[str],
            original_language: str
        ) -> str:
        """Run search for all components of the input analysis."""
        all_results = []
        
        # Search for original English request
        request_results = self.search(request_in_english)
        all_results.extend(self._format_results(request_results))
        
        # Search for each verification fact
        for fact in verification_facts:
            fact_results = self.search(fact)
            all_results.extend(self._format_results(fact_results))
        
        # Search for each question
        for question in possible_questions:
            question_results = self.search(question)
            all_results.extend(self._format_results(question_results))

        # Remove duplicates based on content
        seen_content = set()
        unique_results = []
        for result in all_results:
            if result['content'] not in seen_content:
                seen_content.add(result['content'])
                unique_results.append(result)
        
        all_results = json.dumps(unique_results, indent=2, ensure_ascii=False)
        return all_results
    
    def _format_results(self, docs: List[Document]) -> List[Dict]:
        """Format search results with metadata."""
        return [{
            "wikipedia_article_source": doc.metadata.get('title', 'Unknown title'),
            "content": doc.page_content
        } for doc in docs]