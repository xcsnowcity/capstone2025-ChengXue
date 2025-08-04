#!/usr/bin/env python3

import os
import re
from pathlib import Path
from typing import List, Dict, Any
from bs4 import BeautifulSoup
import chromadb
from sentence_transformers import SentenceTransformer

class SurvivorStoryProcessor:
    
    def __init__(self, stories_path: str = "Knowledge Base/Domestic Abuse Stories"):
        self.stories_path = Path(stories_path)
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Story categories for different types of abuse
        self.abuse_categories = {
            'physical': ['punch', 'kick', 'slap', 'hit', 'push', 'grab', 'violent', 'bruise', 'injury'],
            'emotional': ['control', 'isolate', 'manipulate', 'threaten', 'humiliate', 'gaslight'],  
            'financial': ['money', 'bank', 'income', 'job', 'work', 'financial', 'economic'],
            'coercive_control': ['control', 'monitor', 'restrict', 'isolate', 'permission', 'track'],
            'stalking': ['follow', 'watch', 'harass', 'calls', 'messages', 'social media'],
            'legal': ['court', 'order', 'police', 'solicitor', 'lawyer', 'injunction']
        }
        
        # Hope indicators for recovery stories
        self.hope_indicators = [
            'safe now', 'got help', 'escaped', 'freedom', 'better life', 
            'rebuild', 'recovery', 'support', 'children safe', 'new start'
        ]
    
    def clean_html_content(self, html_content: str) -> str:
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "header", "footer"]):
            script.decompose()
        
        # Get text content
        text = soup.get_text()
        
        # Clean up whitespace and formatting
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Remove browser-specific content
        text = re.sub(r'Read aloud.*?Theme', '', text, flags=re.DOTALL)
        text = re.sub(r'Chrome.*?Firefox', '', text, flags=re.DOTALL)
        text = re.sub(r'font.*?color.*?button', '', text, flags=re.IGNORECASE)
        
        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_story_metadata(self, filename: str, content: str) -> Dict[str, Any]:
        
        # Extract name from filename
        name_match = re.search(r"(.+?)'s Story", filename)
        survivor_name = name_match.group(1) if name_match else "Anonymous"
        
        # Determine organization source
        organization = "NCDV" if "NCDV" in filename else "Domestic Abuse Stories"
        
        # Analyze content for abuse types
        content_lower = content.lower()
        abuse_types = []
        
        for abuse_type, keywords in self.abuse_categories.items():
            if any(keyword in content_lower for keyword in keywords):
                abuse_types.append(abuse_type)
        
        # Check for hope/recovery elements
        has_hope = any(indicator in content_lower for indicator in self.hope_indicators)
        
        # Estimate story length and emotional tone
        word_count = len(content.split())
        
        # Extract key phases (beginning, middle, end)
        story_phases = self.extract_story_phases(content)
        
        return {
            'filename': filename,
            'survivor_name': survivor_name,
            'organization': organization,
            'content_type': 'survivor_story',
            'abuse_types_str': ', '.join(abuse_types),  # Convert list to string
            'primary_abuse_type': abuse_types[0] if abuse_types else 'general',
            'has_hope_element': has_hope,
            'word_count': word_count,
            'audience': 'survivors',
            'topic': 'personal_experience',
            'county': 'National',  # These are general stories, not location-specific
            'trauma_informed': True,
            'validation_provided': True
        }
    
    def extract_story_phases(self, content: str) -> Dict[str, str]:
        
        # Try to identify story structure
        story_phases = {}
        
        # Look for quoted sections (often the survivor's own words)
        quoted_sections = re.findall(r'"([^"]*)"', content)
        quoted_sections.extend(re.findall(r'"([^"]*)"', content))  # Smart quotes
        quoted_sections.extend(re.findall(r"'([^']*)'", content))  # Single quotes
        
        if quoted_sections:
            story_phases['survivor_voice'] = ' '.join(quoted_sections[:3])  # First 3 quotes
        
        # Look for the abuse description
        abuse_patterns = [
            r'(He would .{50,200})',
            r'(I was .{50,200} abused)',
            r'(The abuse .{50,200})',
            r'(physically .{50,200})',
            r'(emotionally .{50,200})'
        ]
        
        for pattern in abuse_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                story_phases['abuse_description'] = match.group(1)
                break
        
        # Look for getting help/recovery
        help_patterns = [
            r'(got help .{50,200})',
            r'(contacted .{50,200})',
            r'(support .{50,200})',
            r'(NCDV .{50,200})',
            r'(refuge .{50,200})'
        ]
        
        for pattern in help_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                story_phases['getting_help'] = match.group(1)
                break
        
        return story_phases
    
    def chunk_survivor_story(self, content: str, metadata: Dict) -> List[Dict[str, Any]]:
        
        chunks = []
        
        # Create different types of chunks for different use cases
        
        # 1. Full story chunk (for comprehensive context)
        full_story_metadata = metadata.copy()
        full_story_metadata.update({
            'chunk_type': 'full_story',
            'chunk_purpose': 'comprehensive_context'
        })
        
        chunks.append({
            'content': content,
            'metadata': full_story_metadata
        })
        
        # 2. Story phases as separate chunks
        story_phases = self.extract_story_phases(content)
        
        for phase_name, phase_content in story_phases.items():
            if phase_content and len(phase_content.strip()) > 50:
                phase_metadata = metadata.copy()
                phase_metadata.update({
                    'chunk_type': 'story_phase',
                    'story_phase': phase_name,
                    'chunk_purpose': 'specific_experience'
                })
                
                chunks.append({
                    'content': phase_content,
                    'metadata': phase_metadata
                })
        
        # 3. Abuse-type specific chunks
        abuse_types_list = metadata.get('abuse_types_str', '').split(', ') if metadata.get('abuse_types_str') else []
        
        for abuse_type in abuse_types_list:
            if abuse_type.strip():
                # Extract sentences related to this abuse type
                abuse_sentences = self.extract_abuse_specific_content(content, abuse_type.strip())
                
                if abuse_sentences:
                    abuse_metadata = metadata.copy()
                    abuse_metadata.update({
                        'chunk_type': 'abuse_specific',
                        'abuse_focus': abuse_type.strip(),
                        'chunk_purpose': 'validation_recognition'
                    })
                    
                    chunks.append({
                        'content': abuse_sentences,
                        'metadata': abuse_metadata
                    })
        
        return chunks
    
    def extract_abuse_specific_content(self, content: str, abuse_type: str) -> str:
        
        keywords = self.abuse_categories.get(abuse_type, [])
        sentences = content.split('.')
        
        relevant_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if any(keyword in sentence.lower() for keyword in keywords):
                relevant_sentences.append(sentence)
        
        return '. '.join(relevant_sentences[:3])  # Limit to 3 sentences
    
    def process_all_stories(self):
        
        print("🏃‍♀️ Processing survivor stories for ChromaDB integration...")
        
        # Get or create collection for survivor stories
        try:
            collection = self.chroma_client.get_collection("domestic_violence_kb")
            print("✅ Using existing ChromaDB collection")
        except:
            print("❌ ChromaDB collection 'domestic_violence_kb' not found")
            print("💡 Run main.py first to create the knowledge base")
            return
        
        processed_count = 0
        total_chunks = 0
        
        # Process each HTML file
        for html_file in self.stories_path.glob("*.html"):
            try:
                print(f"\n📖 Processing: {html_file.name}")
                
                # Read HTML file
                with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                    html_content = f.read()
                
                # Clean and extract text
                clean_content = self.clean_html_content(html_content)
                
                # Skip if content is too short
                if len(clean_content.strip()) < 200:
                    print(f"  ⚠️ Skipped (too short after cleaning)")
                    continue
                
                # Extract metadata
                metadata = self.extract_story_metadata(html_file.name, clean_content)
                
                # Create chunks
                chunks = self.chunk_survivor_story(clean_content, metadata)
                
                # Add chunks to ChromaDB
                for i, chunk in enumerate(chunks):
                    chunk_id = f"survivor_{html_file.stem}_{i}"
                    chunk_metadata = chunk['metadata'].copy()
                    chunk_metadata['chunk_id'] = chunk_id
                    
                    # Create embedding
                    embedding = self.embedding_model.encode(chunk['content']).tolist()
                    
                    # Add to collection
                    collection.add(
                        documents=[chunk['content']],
                        embeddings=[embedding],
                        metadatas=[chunk_metadata],
                        ids=[chunk_id]
                    )
                
                processed_count += 1
                total_chunks += len(chunks)
                
                print(f"  ✅ Added {len(chunks)} chunks")
                print(f"  📊 Abuse types: {metadata['abuse_types_str']}")
                print(f"  💪 Hope element: {'Yes' if metadata['has_hope_element'] else 'No'}")
                
            except Exception as e:
                print(f"  ❌ Error processing {html_file.name}: {e}")
        
        print(f"\n🎉 Processing complete!")
        print(f"📈 Processed {processed_count} survivor stories")
        print(f"📝 Added {total_chunks} story chunks to knowledge base")
        print(f"💾 Total documents in collection: {collection.count()}")
        
        return processed_count, total_chunks
    
    def search_survivor_stories(self, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
        
        collection = self.chroma_client.get_collection("domestic_violence_kb")
        
        # Create query embedding
        query_embedding = self.embedding_model.encode(query).tolist()
        
        # Search with filter for survivor stories
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results * 2,  # Get more results to filter
            include=["documents", "metadatas", "distances"],
            where={"content_type": "survivor_story"}
        )
        
        # Format and filter results
        survivor_stories = []
        for i in range(len(results["documents"][0])):
            story = {
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
                "relevance": 1 - results["distances"][0][i]
            }
            survivor_stories.append(story)
        
        # Sort by relevance and return top results
        survivor_stories.sort(key=lambda x: x["relevance"], reverse=True)
        return survivor_stories[:n_results]


def main():
    
    print("🇮🇪 Irish Domestic Violence Support - Survivor Story Integration")
    print("=" * 70)
    
    # Initialize processor
    processor = SurvivorStoryProcessor()
    
    # Process all stories
    try:
        processed, chunks = processor.process_all_stories()
        
        if processed > 0:
            print(f"\n🧪 Testing story search...")
            
            # Test searches
            test_queries = [
                "physical violence and hitting",
                "getting help and support",
                "controlling behavior",
                "feeling scared and isolated"
            ]
            
            for query in test_queries:
                print(f"\n🔍 Query: '{query}'")
                stories = processor.search_survivor_stories(query, n_results=2)
                
                for story in stories:
                    survivor_name = story['metadata'].get('survivor_name', 'Anonymous')
                    abuse_types = story['metadata'].get('abuse_types_str', 'general')
                    relevance = story['relevance']
                    
                    print(f"  📖 {survivor_name}'s story (Relevance: {relevance:.2f})")
                    print(f"     Types: {abuse_types}")
                    print(f"     Excerpt: {story['content'][:100]}...")
        
        print(f"\n✨ Survivor story integration complete!")
        print(f"💡 Stories are now available for contextual RAG responses")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure the 'Knowledge Base/Domestic Abuse Stories' folder exists")
        print("💡 and that ChromaDB is initialized (run main.py first)")


if __name__ == "__main__":
    main()