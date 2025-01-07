# Search Tools Module: Advanced Search Capabilities for Fact-Checking
# Provides specialized tools for semantic search and metadata retrieval
# Supports multilingual, context-aware information extraction

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
from typing import List, Type, Dict
from .search_manager import SearchManager

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
    
    _vector_store: FAISS = PrivateAttr()
    
    def __init__(self, **data):
        """Initialize RAG tool using SearchManager singleton."""
        super().__init__(**data)
        search_manager = SearchManager()
        self._vector_store = search_manager.vector_store

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

class MetadataSearchTool(BaseTool):
    name: str = "Metadata Search Tool"
    description: str = "Search through documents using the article tittle and returns all its fragments."
    
    _vector_store: FAISS = PrivateAttr()
    result_as_answer: bool = False
    
    def __init__(self, result_as_answer: bool = False, **data):
        """Initialize Metadata Search tool using SearchManager singleton."""
        super().__init__(**data)
        search_manager = SearchManager()
        self._vector_store = search_manager.vector_store
        self.result_as_answer = result_as_answer

    def _run(self, article_title: str) -> str:
        """Run the metadata search tool."""
        try:
            # Normalize the article title for search
            normalized_title = self._normalize_text(article_title)
            docs = self._vector_store.similarity_search(normalized_title, k=5)
            
            # Format results
            results = []
            for doc in docs:
                if self.result_as_answer:
                    results.append(doc.page_content)
                else:
                    results.append({
                        'content': doc.page_content,
                        'metadata': doc.metadata
                    })
            
            return results if not self.result_as_answer else "\n".join(results)
            
        except Exception as e:
            return f"Error searching for article: {str(e)}"

    def _normalize_text(self, text: str) -> str:
        """Normalize text for search."""
        # Remove accents and convert to lowercase
        text = ''.join(c for c in unicodedata.normalize('NFKD', text)
                      if not unicodedata.combining(c))
        text = text.lower()
        
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s]', ' ', text)
        text = ' '.join(text.split())
        
        return text

    def verify_title(self, title: str) -> bool:
        """Verify if a title exists in the database."""
        try:
            docs = self._vector_store.similarity_search(self._normalize_text(title), k=1)
            return bool(docs)
        except:
            return False