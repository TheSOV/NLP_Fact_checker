from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from crewai.tools import BaseTool
from pydantic import BaseModel, Field, PrivateAttr
from typing import List, Type
import os
from pathlib import Path
import re
import unicodedata
from langchain_huggingface import HuggingFaceEmbeddings
import torch

class MetadataSearchInput(BaseModel):
    """Input schema for MetadataSearchTool."""
    title: str = Field(..., description="The title to search for")

class MetadataSearchTool(BaseTool):
    name: str = "Metadata Search Tool"
    description: str = "Search through documents by matching titles, ignoring case, spaces and special characters."
    args_schema: Type[BaseModel] = MetadataSearchInput
    
    _embeddings_path: str = PrivateAttr()
    _vector_store: FAISS = PrivateAttr()
    _all_titles: set = PrivateAttr()
    
    def __init__(self, **data):
        """Initialize Metadata search tool with unified FAISS embeddings."""
        super().__init__(**data)
        
        # Initialize _all_titles set
        self._all_titles = set()
        
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

        for doc in self._vector_store.docstore._dict.values():
            if 'title' in doc.metadata:
                self._all_titles.add(self._normalize_text(doc.metadata['title']))

        print(f"Loaded unified embeddings from {os.path.basename(self._embeddings_path)}")

    def _normalize_text(self, text: str) -> str:
        """Normalize text by removing special characters, spaces, and converting to lowercase.
        
        Args:
            text: The text to normalize
            
        Returns:
            Normalized text string
        """
        # Convert to lowercase
        text = text.lower()
        
        # Normalize unicode characters (e.g., é -> e)
        text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
        
        # Remove special characters and spaces
        text = re.sub(r'[^a-z0-9]', '', text)
        
        return text

    def verify_title(self, title: str) -> bool:
        """Verify if a title is in the list of all titles.
        
        Args:
            title: The title to verify
            
        Returns:
            True if the title is in the list, False otherwise
        """
        return title in self._all_titles
    
    def search_by_title(self, title: str, k: int | None = None) -> List[Document]:
        """Search for documents by title, ignoring case, spaces and special characters.
        
        Args:
            title: The title to search for
            k: Maximum number of documents to return. If None, returns all matches.
            
        Returns:
            List of Document objects that match the title
        """
        # Normalize the search title
        normalized_search_title = self._normalize_text(title)
        
        # Get all documents from the vector store
        all_docs = self._vector_store.docstore._dict.values()
        
        # Filter documents based on normalized titles
        matching_docs = [
            doc for doc in all_docs 
            if 'title' in doc.metadata and 
            self._normalize_text(doc.metadata['title']) == normalized_search_title
        ]
        
        # Limit results if k is specified
        if k is not None:
            matching_docs = matching_docs[:k]
            
        return matching_docs
    
    def _run(self, title: str) -> str:
        """Run title search and return formatted results."""
        # Retrieve matching documents
        matching_docs = self.search_by_title(title, None)
        
        if not matching_docs:
            return f"No documents found with title matching '{title}'"
        
        # Format the results
        results = []
        for doc in matching_docs:
            title = doc.metadata.get('title', 'Unknown title')
            sources = doc.metadata.get('sources', [])
            
            # Format each document with its metadata and content
            fragment = f"[Title: {title}]\n\n{doc.page_content}"
            
            if sources:
                fragment += "\n\nSource:\n"
                fragment += f"Wikipedia Article: {title}"
            
            results.append(fragment)
        
        return "\n\n---\n\n".join(results)