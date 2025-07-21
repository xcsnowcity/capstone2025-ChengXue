#!/usr/bin/env python3
import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv

# Import our knowledge base processor and conversation flow
from main import KnowledgeBaseProcessor
from conversation_flow import ConversationManager, UserProfile, ConversationStage

# LLM imports
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False

# Load environment variables
load_dotenv()

class DomesticViolenceRAG:
    """RAG pipeline specifically designed for domestic violence support in Ireland."""
    
    def __init__(self, 
                 llm_provider: str = "openrouter",  # "openai", "openrouter", or "ollama"
                 model_name: str = "anthropic/claude-3.5-haiku",
                 max_context_chunks: int = 5,
                 temperature: float = 0.3):
        
        self.kb_processor = KnowledgeBaseProcessor()
        self.conversation_manager = ConversationManager()
        self.llm_provider = llm_provider
        self.model_name = model_name
        self.max_context_chunks = max_context_chunks
        self.temperature = temperature
        
        # Initialize LLM client
        if llm_provider == "openai" and OPENAI_AVAILABLE:
            self.openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif llm_provider == "openrouter" and OPENAI_AVAILABLE:
            # OpenRouter uses OpenAI-compatible API
            self.openai_client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"),
            )
        elif llm_provider == "ollama" and OLLAMA_AVAILABLE:
            self.ollama_client = ollama.Client()
        else:
            raise ValueError(f"LLM provider '{llm_provider}' not available or not installed")
        
        # Crisis keywords for safety detection
        self.crisis_keywords = [
            "suicide", "kill myself", "want to die", "end it all", "can't go on",
            "going to hurt", "emergency", "in danger", "threatening me",
            "has a weapon", "going to kill", "immediate danger"
        ]
        
        # Irish-specific system prompt
        self.system_prompt = """You are a compassionate AI assistant helping survivors of domestic violence in Ireland. 

CRITICAL GUIDELINES:
- Use ONLY the provided context from Irish domestic violence organizations
- If information isn't in the context, say "I don't have specific information about that, but [organization] can help"
- Always include relevant contact information when available
- Be trauma-informed: validate feelings, avoid victim-blaming language
- For emergencies, immediately direct to 999/112 and Women's Aid helpline 1800 341 900
- Reference Irish law (Domestic Violence Act 2018) when relevant
- Focus on safety, empowerment, and Irish-specific resources

RESPONSE STRUCTURE:
1. Empathetic acknowledgment
2. Direct answer based on context
3. Relevant Irish contact information
4. Gentle reminder about available support

Remember: You're providing information, not counseling. Encourage professional support."""
    
    def detect_crisis(self, query: str) -> bool:
        """Detect if query contains crisis indicators."""
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in self.crisis_keywords)
    
    def get_crisis_response(self) -> str:
        """Return immediate crisis response."""
        return """🚨 **IMMEDIATE HELP NEEDED**

If you're in immediate danger:
- **Call 999 or 112** for emergency services
- **Women's Aid 24/7 Helpline: 1800 341 900** (free, confidential)

You don't have to face this alone. There are people trained to help you right now.

**Text "Hi" to 50818** for instant message support
**Quick exit this conversation** if needed for your safety"""
    
    def retrieve_context(self, query: str, filter_by: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Retrieve relevant context from knowledge base."""
        
        # Use enhanced search with filters if provided
        results = self.kb_processor.search_knowledge_base(
            query, 
            n_results=self.max_context_chunks
        )
        
        # Filter by metadata if specified
        if filter_by:
            filtered_results = []
            for result in results:
                metadata = result['metadata']
                if all(metadata.get(key) == value for key, value in filter_by.items()):
                    filtered_results.append(result)
            return filtered_results[:self.max_context_chunks]
        
        return results
    
    def format_context(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        """Format retrieved documents for LLM context."""
        
        if not retrieved_docs:
            return "No relevant information found in the knowledge base."
        
        context_parts = []
        
        for i, doc in enumerate(retrieved_docs, 1):
            metadata = doc['metadata']
            organization = metadata['organization']
            content_type = metadata['content_type']
            
            context_parts.append(
                f"--- SOURCE {i}: {organization} ({content_type.upper()}) ---\n"
                f"{doc['content']}\n"
            )
        
        return "\n".join(context_parts)
    
    def generate_response(self, query: str, context: str) -> str:
        """Generate response using LLM with retrieved context."""
        
        # Prepare the prompt
        prompt = f"""CONTEXT FROM IRISH DOMESTIC VIOLENCE ORGANIZATIONS:
{context}

USER QUESTION: {query}

INSTRUCTIONS: Provide a helpful, empathetic response using ONLY the context provided. Include relevant Irish contact information and emphasize safety."""
        
        try:
            if self.llm_provider in ["openai", "openrouter"]:
                response = self.openai_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=500
                )
                return response.choices[0].message.content
            
            elif self.llm_provider == "ollama":
                response = self.ollama_client.chat(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    options={"temperature": self.temperature}
                )
                return response['message']['content']
                
        except Exception as e:
            return f"I'm having trouble generating a response right now. Please contact Women's Aid at 1800 341 900 for immediate support. Error: {str(e)}"
    
    def process_conversational_query(self,
                                   query: str,
                                   user_profile: UserProfile,
                                   current_stage: ConversationStage,
                                   include_sources: bool = True) -> Dict[str, Any]:
        """Process query within conversational context"""
        
        # Check for crisis first
        if self.detect_crisis(query):
            return {
                "response": self.get_crisis_response(),
                "is_crisis": True,
                "sources": [],
                "conversation_stage": ConversationStage.SAFETY_CHECK,
                "profile_update": user_profile,
                "next_prompt": None,
                "metadata": {"crisis_detected": True}
            }
        
        # Get next prompt based on conversation flow
        next_prompt_info = self.conversation_manager.get_next_prompt(
            current_stage, user_profile, query
        )
        
        # If this is a structured prompt (not user query), return it directly
        if next_prompt_info["prompt_type"] in ["safety_assessment", "location_assessment", 
                                             "relationship_assessment", "children_assessment",
                                             "needs_assessment", "crisis_response"]:
            return {
                "response": next_prompt_info["prompt"],
                "is_crisis": False,
                "sources": [],
                "conversation_stage": next_prompt_info["stage"],
                "profile_update": user_profile,
                "next_prompt": next_prompt_info,
                "metadata": {
                    "prompt_type": next_prompt_info["prompt_type"],
                    "profile_completeness": self.conversation_manager.calculate_profile_completeness(user_profile)
                }
            }
        
        # For general queries or when we have enough profile info, use RAG
        if next_prompt_info["prompt_type"] in ["general_query", "personalized_resources"]:
            # Build filter based on user profile
            profile_filter = self.build_profile_filter(user_profile)
            
            # Retrieve context with profile-based filtering
            retrieved_docs = self.retrieve_context(query, profile_filter)
            
            if not retrieved_docs:
                # If no specific results, search without filters
                retrieved_docs = self.retrieve_context(query)
            
            if retrieved_docs:
                # Generate contextual response with conversation awareness
                context = self.format_context(retrieved_docs)
                response = self.generate_conversational_response(query, context, user_profile)
            else:
                # Fallback to personalized generic response
                response = self.conversation_manager.generate_personalized_response(user_profile)
            
            # Prepare sources
            sources = []
            for doc in retrieved_docs:
                metadata = doc['metadata']
                sources.append({
                    "organization": metadata['organization'],
                    "filename": metadata['filename'],
                    "content_type": metadata['content_type'],
                    "relevance": 1 - doc['distance']
                })
            
            return {
                "response": response,
                "is_crisis": False,
                "sources": sources,
                "conversation_stage": next_prompt_info["stage"],
                "profile_update": user_profile,
                "next_prompt": next_prompt_info,
                "metadata": {
                    "num_sources": len(retrieved_docs),
                    "profile_completeness": self.conversation_manager.calculate_profile_completeness(user_profile),
                    "personalized": True,
                    "used_rag": True
                }
            }
        
        # Fallback - shouldn't reach here, but just in case
        return self.process_query(query, self.build_profile_filter(user_profile), include_sources)
    
    def build_profile_filter(self, user_profile: UserProfile) -> Optional[Dict]:
        """Build metadata filter based on user profile"""
        filter_criteria = {}
        
        # Filter by county if known
        if user_profile.county:
            filter_criteria["county"] = user_profile.county.title()
        
        # Filter by content type based on primary concern
        if user_profile.primary_concern:
            content_type_mapping = {
                "legal_information": "legal",
                "safety_planning": "safety",
                "emotional_support": "support",
                "practical_resources": "support"
            }
            if user_profile.primary_concern in content_type_mapping:
                filter_criteria["content_type"] = content_type_mapping[user_profile.primary_concern]
        
        return filter_criteria if filter_criteria else None
    
    def generate_conversational_response(self, query: str, context: str, user_profile: UserProfile) -> str:
        """Generate response with conversational context"""
        
        # Build personalized system prompt
        profile_context = self.build_profile_context(user_profile)
        
        enhanced_system_prompt = f"""{self.system_prompt}

CONVERSATION CONTEXT:
{profile_context}

PERSONALIZATION GUIDELINES:
- Reference their location ({user_profile.location or 'Ireland'}) when relevant
- Consider their relationship status and living situation
- If they have children, prioritize family-focused resources
- Match the tone to their expressed needs and concerns
- Build on information they've already shared"""
        
        # Prepare the prompt
        prompt = f"""CONTEXT FROM IRISH DOMESTIC VIOLENCE ORGANIZATIONS:
{context}

USER QUESTION: {query}

CONVERSATION HISTORY: Based on our conversation, I know this person is in {user_profile.location or 'Ireland'}{', has children' if user_profile.has_children else ''}{', and is primarily concerned about ' + user_profile.primary_concern if user_profile.primary_concern else ''}.

INSTRUCTIONS: Provide a personalized, empathetic response using the context. Reference their specific situation when relevant."""
        
        try:
            if self.llm_provider in ["openai", "openrouter"]:
                response = self.openai_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": enhanced_system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=600
                )
                return response.choices[0].message.content
            
            elif self.llm_provider == "ollama":
                response = self.ollama_client.chat(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": enhanced_system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    options={"temperature": self.temperature}
                )
                return response['message']['content']
                
        except Exception as e:
            return f"I'm having trouble generating a response right now. Please contact Women's Aid at 1800 341 900 for immediate support. Error: {str(e)}"
    
    def build_profile_context(self, user_profile: UserProfile) -> str:
        """Build context string from user profile"""
        context_parts = []
        
        if user_profile.location:
            context_parts.append(f"Location: {user_profile.location}")
        
        if user_profile.relationship_status:
            context_parts.append(f"Relationship status: {user_profile.relationship_status}")
        
        if user_profile.has_children is not None:
            context_parts.append(f"Has children: {'Yes' if user_profile.has_children else 'No'}")
        
        if user_profile.safety_level:
            context_parts.append(f"Safety level: {user_profile.safety_level.value}")
        
        if user_profile.primary_concern:
            context_parts.append(f"Primary concern: {user_profile.primary_concern}")
        
        return "; ".join(context_parts) if context_parts else "Initial conversation"

    def process_query(self, 
                     query: str, 
                     filter_by: Optional[Dict] = None,
                     include_sources: bool = True) -> Dict[str, Any]:
        """Main RAG pipeline: retrieve context and generate response."""
        
        # Check for crisis indicators first
        if self.detect_crisis(query):
            return {
                "response": self.get_crisis_response(),
                "is_crisis": True,
                "sources": [],
                "metadata": {"crisis_detected": True}
            }
        
        # Retrieve relevant context
        retrieved_docs = self.retrieve_context(query, filter_by)
        
        if not retrieved_docs:
            return {
                "response": """I don't have specific information about that in my knowledge base, but you can get help from:

**Women's Aid 24/7 Helpline: 1800 341 900** (free, confidential)
**Safe Ireland:** safeireland.ie
**Citizens Information:** citizensinformation.ie

These organizations have comprehensive information and trained support staff.""",
                "is_crisis": False,
                "sources": [],
                "metadata": {"no_context_found": True}
            }
        
        # Format context for LLM
        context = self.format_context(retrieved_docs)
        
        # Generate response
        response = self.generate_response(query, context)
        
        # Prepare sources for citation
        sources = []
        if include_sources:
            for doc in retrieved_docs:
                metadata = doc['metadata']
                sources.append({
                    "organization": metadata['organization'],
                    "filename": metadata['filename'],
                    "content_type": metadata['content_type'],
                    "relevance": 1 - doc['distance']
                })
        
        return {
            "response": response,
            "is_crisis": False,
            "sources": sources,
            "metadata": {
                "num_sources": len(retrieved_docs),
                "query_length": len(query),
                "context_length": len(context)
            }
        }

def demo_rag_pipeline():
    """Demonstrate the RAG pipeline with sample queries."""
    
    print("🇮🇪 Irish Domestic Violence RAG Pipeline Demo")
    print("=" * 60)
    print("⚠️  Note: This demo uses local models. For production, consider OpenAI/Claude for better responses.")
    print()
    
    # Initialize RAG pipeline
    try:
        rag = DomesticViolenceRAG(llm_provider="ollama", model_name="llama3.2")
        print("✅ RAG pipeline initialized with Ollama")
    except Exception as e:
        print(f"❌ Could not initialize RAG pipeline: {e}")
        print("💡 Make sure you have Ollama installed and llama3.2 model downloaded")
        print("   Run: ollama pull llama3.2")
        return
    
    # Test queries
    test_queries = [
        "What is coercive control under Irish law?",
        "How can I get a safety order?",
        "I'm in Dublin and need support services",
        "I want to kill myself",  # Crisis test
        "What financial help is available for survivors?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 Query {i}: '{query}'")
        print("-" * 50)
        
        try:
            result = rag.process_query(query)
            
            if result['is_crisis']:
                print("🚨 CRISIS DETECTED")
            
            print(f"📝 Response:\n{result['response']}")
            
            if result['sources']:
                print(f"\n📚 Sources ({len(result['sources'])}):")
                for j, source in enumerate(result['sources'][:3], 1):
                    print(f"  {j}. [{source['organization']}] {source['content_type']} "
                          f"(Relevance: {source['relevance']:.2f})")
            
        except Exception as e:
            print(f"❌ Error processing query: {e}")
    
    print(f"\n" + "=" * 60)
    print("✅ RAG Pipeline Demo Complete")
    print("🔄 Ready for integration with Open WebUI or other chat interfaces")

if __name__ == "__main__":
    demo_rag_pipeline()