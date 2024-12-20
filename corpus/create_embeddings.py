from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from pathlib import Path
import os
import xml.etree.ElementTree as ET
import re
import torch

def extract_article_info(xml_path: str) -> list[dict]:
    """
    Extract title, text, and sources from Wikipedia XML file.
    """
    
    # Register the namespace
    namespaces = {
        'mw': 'http://www.mediawiki.org/xml/export-0.11/'
    }
    
    tree = ET.parse(xml_path)
    root = tree.getroot()
    articles = []
    total_articles = 0
    valid_articles = 0
    
    # Use the namespace in findall
    for page in root.findall('.//mw:page', namespaces):
        total_articles += 1
        
        try:
            # Extract title
            title_elem = page.find('.//mw:title', namespaces)
            if title_elem is None or not title_elem.text:
                continue
            title = title_elem.text.strip()
            
            # Extract text content
            text_elem = page.find('.//mw:revision/mw:text', namespaces)
            if text_elem is None or not text_elem.text:
                continue
            
            text = text_elem.text

            if len(text) < 500:
                continue
            
            # Clean up the text by removing Wiki markup
            # Remove reference tags but capture their content first
            sources = []
            if '<ref' in text:
                ref_pattern = r'<ref[^>]*>(.*?)</ref>'
                sources = re.findall(ref_pattern, text, re.DOTALL)
                # Clean up sources
                sources = [s.strip() for s in sources if s.strip()]
            
            # Remove Wiki markup
            text = re.sub(r'<ref.*?</ref>', '', text, flags=re.DOTALL)  # Remove reference tags
            text = re.sub(r'\{\{[^\}]*\}\}', '', text, flags=re.DOTALL)  # Remove templates
            text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', text)  # Convert [[link|text]] to text
            text = re.sub(r'\[https?://[^\]]*\]', '', text)  # Remove external links
            text = re.sub(r"''+", '', text)  # Remove bold/italic markers
            text = re.sub(r'={2,}.*?={2,}', '', text)  # Remove section headers
            text = re.sub(r'__[A-Z]+__', '', text)  # Remove magic words
            
            # Clean up whitespace
            text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())
            
            # Skip empty articles
            if not text:
                continue
            
            articles.append({
                "title": title,
                "content": text,
                "sources": sources[:5]  # Keep only first 5 sources to save memory
            })
            valid_articles += 1
            
            # Print progress every 100 valid articles
            if valid_articles % 100 == 0:
                print(f"Processed {valid_articles} valid articles out of {total_articles} total articles...")
        
        except Exception as e:
            print(f"Error processing article: {str(e)}")
            continue
    
    print(f"\nFile summary:")
    print(f"Total articles found: {total_articles}")
    print(f"Valid articles: {valid_articles}")
    print(f"Articles skipped: {total_articles - valid_articles}")
    
    return articles

def process_xml_file(xml_path: str) -> list[Document]:
    """Process a single XML file and return document chunks."""
    # Extract articles from XML
    articles = extract_article_info(xml_path)
    
    if not articles:
        print(f"Warning: No valid articles found in {Path(xml_path).name}")
        return []
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    
    all_splits = []
    for article in articles:
        # Create metadata
        metadata = {
            "title": article["title"],
            "sources": article["sources"][:5]  # Store up to 5 sources in metadata
        }
        
        # Split the content into chunks
        splits = text_splitter.create_documents(
            texts=[article["content"]],
            metadatas=[metadata]
        )
        all_splits.extend(splits)
    
    print(f"Created {len(all_splits)} chunks from {len(articles)} articles in {Path(xml_path).name}")
    return all_splits

def create_unified_embeddings(xml_dir: str, save_path: str) -> None:
    """Create and save a single FAISS index for all XML files."""
    # Initialize embeddings with sentence-transformers, using GPU if available
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu'}
    )
    all_splits = []
    
    # Process each XML file
    xml_files = [f for f in os.listdir(xml_dir) if 'xml' in f.lower()]
    print(f"\nFound {len(xml_files)} XML files to process")
    
    for file in xml_files:
        xml_path = os.path.join(xml_dir, file)
        splits = process_xml_file(xml_path)
        all_splits.extend(splits)
    
    if not all_splits:
        raise ValueError("No valid articles found in any XML files. Cannot create embeddings.")
    
    print(f"\nTotal chunks across all files: {len(all_splits)}")
    
    # Create unified vector store with progress tracking
    print("\nCreating FAISS index...")
    total_chunks = len(all_splits)
    batch_size = 100  # Process in batches to show progress
    vector_store = None
    
    for i in range(0, total_chunks, batch_size):
        batch = all_splits[i:i + batch_size]
        print(f"Processing embeddings batch {i//batch_size + 1}/{(total_chunks + batch_size - 1)//batch_size} ({i}/{total_chunks} documents)")
        
        # Create or extend the vector store
        if vector_store is None:
            vector_store = FAISS.from_documents(batch, embeddings)
        else:
            batch_vectorstore = FAISS.from_documents(batch, embeddings)
            vector_store.merge_from(batch_vectorstore)
    
    # Create save directory if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # Save vector store
    vector_store.save_local(save_path)
    print(f"\nSaved unified embeddings to {save_path}")

if __name__ == "__main__":
    # Get the absolute path to the corpus directory
    corpus_dir = os.path.dirname(os.path.abspath(__file__))
    unzipped_dir = os.path.join(corpus_dir, "unzipped")
    embeddings_dir = os.path.join(corpus_dir, "embeddings", "unified_index")
    
    # Create and save embeddings
    create_unified_embeddings(unzipped_dir, embeddings_dir)
