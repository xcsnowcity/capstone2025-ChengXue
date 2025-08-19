import os
import re
import json
from pathlib import Path
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
import tiktoken
from sentence_transformers import SentenceTransformer

class KnowledgeBaseProcessor:
    def __init__(self, knowledge_base_path: str = "Knowledge Base"):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        
    def clean_markdown_content(self, content: str) -> str:
        # Clean markdown content by removing navigation, cookies, and web artifacts.

        # Remove cookie consent sections
        content = re.sub(r'Google Webfont Settings:.*?Notifications', '', content, flags=re.DOTALL)
        content = re.sub(r'We also use different external services.*?Hide notification only.*?\n', '', content, flags=re.DOTALL)
        
        # Remove navigation elements
        content = re.sub(r'^\s*\*\s*\[.*?\]\(.*?\)\s*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'^\s*\d+\.\s*\[.*?\]\(.*?\)\s*$', '', content, flags=re.MULTILINE)
        
        # Remove "Skip to main content" and similar links
        content = re.sub(r'\[Skip to main content\].*?\n', '', content)
        content = re.sub(r'\[Quick exit\].*?\n', '', content)
        content = re.sub(r'\[Back to top of page\].*?\n', '', content)
        
        # Remove image alt text and links
        content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
        content = re.sub(r'^\s*\[.*?\]\(.*?\)\s*$', '', content, flags=re.MULTILINE)
        
        # Remove social media links
        content = re.sub(r'^\s*\*\s*\[(?:X|Facebook|Twitter|Instagram|LinkedIn).*?\]\(.*?\)', '', content, flags=re.MULTILINE)
        
        # Remove search and menu elements
        content = re.sub(r'Search\s*Search', '', content)
        content = re.sub(r'Menu\s*Menu', '', content)
        
        # Remove privacy policy footers
        content = re.sub(r'Privacy Policy.*?$', '', content, flags=re.DOTALL)
        content = re.sub(r'\[Privacy\].*?$', '', content, flags=re.DOTALL)
        
        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        content = re.sub(r'^\s+', '', content, flags=re.MULTILINE)
        
        # Remove empty lines at start and end
        content = content.strip()
        
        return content
    
    def chunk_content(self, content: str, max_tokens: int = 500, overlap: int = 50) -> List[str]:
        # Chunk content into smaller pieces with overlap.

        # Split by paragraphs first
        paragraphs = content.split('\n\n')
        chunks = []
        current_chunk = ""
        current_tokens = 0
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
                
            paragraph_tokens = len(self.tokenizer.encode(paragraph))
            
            # If paragraph is too long, split it further
            if paragraph_tokens > max_tokens:
                sentences = paragraph.split('. ')
                for sentence in sentences:
                    sentence = sentence.strip()
                    if not sentence:
                        continue
                    
                    sentence_tokens = len(self.tokenizer.encode(sentence))
                    
                    if current_tokens + sentence_tokens > max_tokens:
                        if current_chunk:
                            chunks.append(current_chunk.strip())
                        current_chunk = sentence
                        current_tokens = sentence_tokens
                    else:
                        current_chunk += f" {sentence}"
                        current_tokens += sentence_tokens
            else:
                if current_tokens + paragraph_tokens > max_tokens:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = paragraph
                    current_tokens = paragraph_tokens
                else:
                    current_chunk += f"\n\n{paragraph}"
                    current_tokens += paragraph_tokens
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def extract_metadata(self, file_path: Path) -> Dict[str, Any]:
        # Extract metadata from file path and content.

        parts = file_path.parts
        metadata = {
            "file_path": str(file_path),
            "filename": file_path.name,
            "organization": "Unknown",
            "county": "National",
            "topic": "General",
            "content_type": "general"
        }
        
        # Determine organization
        if "safeireland" in str(file_path):
            metadata["organization"] = "Safe Ireland"
        elif "womensaid" in str(file_path):
            metadata["organization"] = "Women's Aid"
        elif "hse" in str(file_path):
            metadata["organization"] = "HSE"
        
        # Extract county information
        counties = [
            "carlow", "cavan", "clare", "cork", "donegal", "dublin",
            "galway", "kerry", "kildare", "kilkenny", "laois", "leitrim",
            "limerick", "longford", "louth", "mayo", "meath", "monaghan",
            "offaly", "roscommon", "sligo", "tipperary", "waterford",
            "westmeath", "wexford", "wicklow"
        ]
        
        for county in counties:
            if county in str(file_path).lower():
                metadata["county"] = county.title()
                break
        
        # Determine content type based on path
        path_str = str(file_path).lower()
        if "safety" in path_str or "protection" in path_str:
            metadata["content_type"] = "safety"
        elif "legal" in path_str or "court" in path_str or "order" in path_str:
            metadata["content_type"] = "legal"
        elif "support" in path_str or "help" in path_str:
            metadata["content_type"] = "support"
        elif "understanding" in path_str or "what-is" in path_str:
            metadata["content_type"] = "education"
        
        return metadata
    
    def process_knowledge_base(self, force_reprocess=False):
        # Process all markdown files in the knowledge base.

        print("Processing knowledge base...")
        
        # Create or get collection
        try:
            collection = self.chroma_client.get_collection("domestic_violence_kb")
            print("Using existing collection")
            # Get list of already processed files
            existing_ids = set(collection.get()['ids']) if not force_reprocess else set()
        except:
            collection = self.chroma_client.create_collection(
                name="domestic_violence_kb",
                metadata={"description": "Irish domestic violence knowledge base"}
            )
            print("Created new collection")
            existing_ids = set()
        
        processed_count = 0
        skipped_count = 0
        
        # Process all markdown files
        for md_file in self.knowledge_base_path.rglob("*.md"):
            try:
                # Check if file already processed
                file_base_id = f"{md_file.stem}_0"
                if file_base_id in existing_ids:
                    print(f"Skipping (already processed): {md_file.name}")
                    skipped_count += 1
                    continue
                
                print(f"Processing: {md_file.name}")
                
                # Read file
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Clean content
                cleaned_content = self.clean_markdown_content(content)
                
                # Skip if content is too short after cleaning
                if len(cleaned_content.strip()) < 100:
                    print(f"  Skipped (too short after cleaning)")
                    continue
                
                # Chunk content
                chunks = self.chunk_content(cleaned_content)
                
                # Extract metadata
                metadata = self.extract_metadata(md_file)
                
                # Process each chunk
                for i, chunk in enumerate(chunks):
                    chunk_id = f"{md_file.stem}_{i}"
                    chunk_metadata = metadata.copy()
                    chunk_metadata["chunk_id"] = chunk_id
                    chunk_metadata["chunk_index"] = i
                    chunk_metadata["total_chunks"] = len(chunks)
                    
                    # Create embedding
                    embedding = self.embedding_model.encode(chunk).tolist()
                    
                    # Add to collection
                    collection.add(
                        documents=[chunk],
                        embeddings=[embedding],
                        metadatas=[chunk_metadata],
                        ids=[chunk_id]
                    )
                
                processed_count += 1
                print(f"  Added {len(chunks)} chunks")
                
            except Exception as e:
                print(f"  Error processing {md_file.name}: {e}")
        
        print(f"\nProcessed {processed_count} new files, skipped {skipped_count} existing files")
        print(f"Collection now has {collection.count()} documents")
    
    def reset_knowledge_base(self):
        # Delete and recreate the knowledge base from scratch.
        print("Resetting knowledge base...")
        try:
            self.chroma_client.delete_collection("domestic_violence_kb")
            print("Deleted existing collection")
        except:
            print("No existing collection to delete")
        
        # Reprocess everything
        self.process_knowledge_base(force_reprocess=True)
    
    def search_knowledge_base(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        # Search the knowledge base for relevant content.

        collection = self.chroma_client.get_collection("domestic_violence_kb")
        
        # Create query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results["documents"][0])):
            formatted_results.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })
        
        return formatted_results

def main():
    # Main function to process knowledge base or run searches.

    processor = KnowledgeBaseProcessor()
    
    # Check if we should process the knowledge base
    if not os.path.exists("./chroma_db"):
        print("ChromaDB not found. Processing knowledge base...")
        processor.process_knowledge_base()
    else:
        print("ChromaDB found. Ready for queries.")
        
        # Interactive search mode
        while True:
            query = input("\nEnter your question (or 'quit' to exit): ")
            if query.lower() == 'quit':
                break
            
            if query.strip():
                print("\nSearching knowledge base...")
                results = processor.search_knowledge_base(query)
                
                print(f"\nTop {len(results)} results:")
                for i, result in enumerate(results, 1):
                    print(f"\n{i}. [{result['metadata']['organization']}] "
                          f"{result['metadata']['filename']}")
                    print(f"   Distance: {result['distance']:.3f}")
                    print(f"   Content: {result['content'][:200]}...")

if __name__ == "__main__":
    main()