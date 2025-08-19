#!/usr/bin/env python3
import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
# Try to load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Continue without dotenv

# Import our knowledge base processor and conversation flow
from main import KnowledgeBaseProcessor
from conversation_flow import ConversationManager, UserProfile, ConversationStage
from llm_crisis_detector import LLMCrisisDetector, CrisisLevel
from trauma_informed_delivery import TraumaInformedDelivery, NarrativeType, TraumaRisk

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

class DomesticViolenceRAG:
    def __init__(self, 
                 llm_provider: str = "openrouter",  # "openai", "openrouter", or "ollama"
                 model_name: str = "anthropic/claude-3.5-haiku",
                 max_context_chunks: int = 5,
                 temperature: float = 0.3):
        
        self.kb_processor = KnowledgeBaseProcessor()
        self.conversation_manager = ConversationManager()
        self.trauma_delivery = TraumaInformedDelivery()
        self.crisis_detector = LLMCrisisDetector(llm_provider, model_name)
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
        
        # Irish-specific system prompt with survivor story integration
        self.system_prompt = """You are a compassionate AI assistant helping survivors of domestic violence in Ireland. 

CRITICAL GUIDELINES:
- Use ONLY the provided context from Irish domestic violence organizations
- If information isn't in the context, say "I don't have specific information about that, but [organization] can help"
- Always include relevant contact information when available
- Be trauma-informed: validate feelings, avoid victim-blaming language
- For emergencies, immediately direct to 999/112 and Women's Aid helpline 1800 341 900
- Reference Irish law (Domestic Violence Act 2018) when relevant
- Focus on safety, empowerment, and Irish-specific resources

SURVIVOR STORY INTEGRATION:
- When survivor stories are provided, use them thoughtfully for validation and hope
- Frame survivor experiences as "others have experienced similar situations"
- Highlight recovery/hope elements from stories when appropriate
- Never identify survivors by real names (use "one survivor" or similar)
- Balance informational content with lived experience validation
- Use stories to show that abuse follows patterns and recovery is possible

RESPONSE STRUCTURE:
1. Empathetic acknowledgment
2. Direct answer based on informational context
3. Relevant validation from survivor experiences (if applicable)
4. Relevant Irish contact information
5. Gentle reminder about available support and hope for recovery

Remember: You're providing information, not counseling. Encourage professional support."""
    
    def detect_crisis(self, query: str) -> bool:
        # Detect if query contains crisis indicators using enhanced LLM detection.
        crisis_result = self.crisis_detector.detect_crisis_hybrid(query)
        
        # Consider high-risk and immediate danger as crisis
        return crisis_result.crisis_level in [CrisisLevel.IMMEDIATE_DANGER, CrisisLevel.HIGH_RISK]
    
    def get_detailed_crisis_info(self, query: str) -> dict:
        # Get detailed crisis analysis for enhanced responses.
        crisis_result = self.crisis_detector.detect_crisis_hybrid(query)
        return {
            "is_crisis": crisis_result.crisis_level in [CrisisLevel.IMMEDIATE_DANGER, CrisisLevel.HIGH_RISK],
            "crisis_level": crisis_result.crisis_level.value,
            "confidence": crisis_result.confidence,
            "reasoning": crisis_result.reasoning,
            "immediate_action_needed": crisis_result.immediate_action_needed,
            "triggered_by": crisis_result.triggered_by
        }
    
    def get_crisis_response(self) -> str:
        return """🚨 **IMMEDIATE HELP NEEDED**

If you're in immediate danger:
- **Call 999 or 112** for emergency services
- **Women's Aid 24/7 Helpline: 1800 341 900** (free, confidential)

You don't have to face this alone. There are people trained to help you right now.

**Text "Hi" to 50818** for instant message support
**Quick exit this conversation** if needed for your safety"""
    
    def get_moderate_risk_response(self) -> str:
        # Response for moderate risk situations - still needs DV-specific support
        return """I hear the strength it took to reach out, and I want you to know you're not alone in feeling this way.

**First, are you in a safe place right now to talk?**

Many people in difficult relationships feel overwhelmed - these feelings are completely valid. You deserve support and safety.

**Immediate Support Available:**
- **Women's Aid 24/7 Helpline: 1800 341 900** (free, confidential)
- **Text "Hi" to 50818** for instant message support
- **Emergency: 999 or 112** if you feel unsafe

**I can help you with:**
- Understanding your rights and options in Ireland
- Safety planning information
- Local support services in your area
- Information about court orders and legal processes

What would be most helpful for you right now? Remember, you can exit this conversation quickly using the button above if needed for your safety."""
    
    def get_low_risk_response_with_safety_check(self) -> str:
        # Response for low-risk situations but still with safety awareness
        return """Thank you for reaching out. **Are you in a safe place right now?**

I'm here to provide information about domestic violence support and resources in Ireland.

**Support Always Available:**
- **Women's Aid 24/7 Helpline: 1800 341 900** (free, confidential)
- **Emergency: 999 or 112** if needed

**I can help you with:**
- Understanding domestic violence and your rights
- Information about support services in your area
- Legal options and court processes
- Safety planning information

What information would be most helpful to you?"""
    
    def retrieve_context(self, query: str, filter_by: Optional[Dict] = None) -> List[Dict[str, Any]]:
        
        # Check if query would benefit from survivor narratives
        include_survivor_stories = self.should_include_survivor_stories(query)
        
        # Use enhanced search with filters if provided
        results = self.kb_processor.search_knowledge_base(
            query, 
            n_results=self.max_context_chunks * 2  # Get more to allow filtering
        )
        
        # Separate survivor stories from informational content
        informational_results = []
        survivor_story_results = []
        
        for result in results:
            metadata = result['metadata']
            content_type = metadata.get('content_type', '')
            
            # Apply general filters if specified
            if filter_by:
                if not all(metadata.get(key) == value for key, value in filter_by.items()):
                    continue
            
            if content_type == 'survivor_story':
                survivor_story_results.append(result)
            else:
                informational_results.append(result)
        
        # Balance content types based on query with trauma-informed filtering
        final_results = []
        
        if include_survivor_stories and survivor_story_results:
            # Include 1-2 survivor stories for validation/hope with trauma screening
            relevant_stories = self.select_relevant_survivor_stories(query, survivor_story_results)
            
            # Apply trauma-informed filtering
            safe_stories = []
            for story in relevant_stories[:2]:
                validation_result = self.trauma_delivery.validate_story_delivery(
                    {'content': story['content'], 'metadata': story['metadata']},
                    user_vulnerability="moderate"  # Default to moderate caution
                )
                
                if validation_result['should_deliver']:
                    # Add trauma-informed framing to metadata
                    story['trauma_framing'] = validation_result.get('framing', {})
                    safe_stories.append(story)
            
            final_results.extend(safe_stories)
            
            # Fill remaining slots with informational content
            remaining_slots = self.max_context_chunks - len(final_results)
            final_results.extend(informational_results[:remaining_slots])
        else:
            # Primarily informational content
            final_results = informational_results[:self.max_context_chunks]
        
        return final_results
    
    def should_include_survivor_stories(self, query: str) -> bool:
        query_lower = query.lower()
        
        # Keywords that suggest need for validation or hope
        validation_keywords = [
            'alone', 'scared', 'isolated', 'ashamed', 'fault', 'blame', 'crazy',
            'overreacting', 'deserved', 'worthless', 'stupid', 'embarrassed',
            'no one believes', 'not that bad', 'making it up', 'am i'
        ]
        
        hope_keywords = [
            'hopeless', 'never get better', 'never escape', 'trapped', 'no way out',
            'will it get better', 'is there hope', 'hope', 'success stories', 
            'recovered', 'recovery', 'life after abuse', 'healing', 'moving on', 
            'got out', 'better', 'escape', 'freedom'
        ]
        
        experience_keywords = [
            'hits', 'hit', 'punch', 'slap', 'hurt', 'violence', 'violent',
            'control', 'controls', 'controlling', 'monitor', 'monitors',
            'jealous', 'isolat', 'money', 'financial', 'coercive', 
            'gaslight', 'manipulat', 'threat', 'scare', 'afraid'
        ]
        
        personal_indicators = [
            'i feel', 'i am', 'i\'m', 'he does', 'she does', 'my partner',
            'my husband', 'my wife', 'my boyfriend', 'my girlfriend', 
            'he is', 'she is', 'he makes', 'she makes'
        ]
        
        # Check for validation needs (emotional support keywords)
        validation_found = any(keyword in query_lower for keyword in validation_keywords)
        
        # Check for hope/recovery needs
        hope_found = any(keyword in query_lower for keyword in hope_keywords)
        
        # Check for personal experience sharing
        experience_found = any(keyword in query_lower for keyword in experience_keywords)
        personal_found = any(indicator in query_lower for indicator in personal_indicators)
        
        # Experience + personal indicators suggest need for validation
        if experience_found and personal_found:
            return True
        
        # Direct validation or hope needs
        if validation_found or hope_found:
            return True
        
        # Legal/informational queries should NOT include stories by default
        legal_keywords = ['court', 'order', 'law', 'legal', 'solicitor', 'lawyer', 'apply', 'process']
        if any(keyword in query_lower for keyword in legal_keywords) and not (validation_found or hope_found):
            return False
        
        return False
    
    def select_relevant_survivor_stories(self, query: str, survivor_stories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        query_lower = query.lower()
        scored_stories = []
        
        for story in survivor_stories:
            metadata = story['metadata']
            content = story['content'].lower()
            score = 0
            
            # Score based on abuse type matching
            abuse_types = metadata.get('abuse_types_str', '').lower()
            if abuse_types:
                abuse_type_list = [t.strip() for t in abuse_types.split(',')]
                for abuse_type in abuse_type_list:
                    if abuse_type and abuse_type in query_lower:
                        score += 2  # High weight for abuse type match
            
            # Score based on hope elements if query suggests hopelessness
            hope_indicators = ['hopeless', 'trapped', 'no way out', 'will it get better']
            if any(indicator in query_lower for indicator in hope_indicators):
                if metadata.get('has_hope_element', False):
                    score += 3  # Very high weight for hope when needed
            
            # Score based on content relevance (basic keyword matching)
            query_words = set(query_lower.split())
            content_words = set(content.split())
            common_words = query_words.intersection(content_words)
            score += len(common_words) * 0.1  # Small weight for word overlap
            
            # Prefer full stories over chunks for better narrative flow
            chunk_type = metadata.get('chunk_type', '')
            if chunk_type == 'full_story':
                score += 1
            elif chunk_type == 'story_phase':
                score += 0.5
            
            scored_stories.append((score, story))
        
        # Sort by score and return top stories
        scored_stories.sort(key=lambda x: x[0], reverse=True)
        return [story for _, story in scored_stories]
    
    def format_context(self, retrieved_docs: List[Dict[str, Any]]) -> str:
        if not retrieved_docs:
            return "No relevant information found in the knowledge base."
        
        context_parts = []
        informational_docs = []
        survivor_stories = []
        
        # Separate different content types
        for doc in retrieved_docs:
            metadata = doc['metadata']
            if metadata.get('content_type') == 'survivor_story':
                survivor_stories.append(doc)
            else:
                informational_docs.append(doc)
        
        # Format informational content first
        for i, doc in enumerate(informational_docs, 1):
            metadata = doc['metadata']
            organization = metadata['organization']
            content_type = metadata['content_type']
            
            context_parts.append(
                f"--- INFORMATION SOURCE {i}: {organization} ({content_type.upper()}) ---\n"
                f"{doc['content']}\n"
            )
        
        # Format survivor stories with trauma-informed treatment
        for i, doc in enumerate(survivor_stories, 1):
            metadata = doc['metadata']
            survivor_name = metadata.get('survivor_name', 'Anonymous')
            abuse_types = metadata.get('abuse_types_str', 'general abuse')
            chunk_type = metadata.get('chunk_type', 'story')
            has_hope = metadata.get('has_hope_element', False)
            
            # Use trauma-informed framing if available
            trauma_framing = doc.get('trauma_framing', {})
            
            hope_indicator = " [RECOVERY STORY]" if has_hope else ""
            
            # Include trauma-informed context
            story_context = f"--- SURVIVOR EXPERIENCE {i}: {survivor_name}'s Story{hope_indicator} ---\n"
            story_context += f"Abuse types: {abuse_types}\n"
            story_context += f"Story type: {chunk_type}\n"
            
            # Add framing guidance if available
            if trauma_framing:
                if 'introduction' in trauma_framing:
                    story_context += f"Framing: {trauma_framing['introduction']}\n"
                if 'content_warning' in trauma_framing:
                    story_context += f"Content Note: {trauma_framing['content_warning']}\n"
            
            # Use processed content if available, otherwise original
            story_content = trauma_framing.get('processed_content', doc['content'])
            story_context += f"Content: {story_content}\n"
            
            # Add empowerment message if available
            if trauma_framing.get('empowerment_message'):
                story_context += f"Key Message: {trauma_framing['empowerment_message']}\n"
            
            context_parts.append(story_context)
        
        return "\n".join(context_parts)
    
    def generate_response(self, query: str, context: str) -> str:
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
                                   include_sources: bool = True,
                                   response_length: str = "adaptive") -> Dict[str, Any]:

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
                response = self.generate_conversational_response(query, context, user_profile, response_length)
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
    
    def generate_conversational_response(self, query: str, context: str, user_profile: UserProfile, response_length: str = "adaptive") -> str:

        # Build personalized system prompt
        profile_context = self.build_profile_context(user_profile)
        
        # Response length instructions
        length_instructions = {
            "brief": """
RESPONSE LENGTH: BRIEF (2-3 sentences + 1 key contact)
- Provide a concise, direct answer
- Include only the most essential information
- End with one relevant contact number
- Use bullet points for clarity if needed
- Maximum 150 words""",
            
            "detailed": """
RESPONSE LENGTH: COMPREHENSIVE 
- Provide thorough, step-by-step information
- Include relevant background context
- List multiple resources and contacts
- Explain procedures in detail
- Include examples where helpful""",
            
            "adaptive": """
RESPONSE LENGTH: ADAPTIVE (balanced - default)
- Provide helpful information without overwhelming
- Include 2-3 key points
- Add relevant contacts
- Balance detail with accessibility
- Aim for 200-300 words"""
        }
        
        enhanced_system_prompt = f"""{self.system_prompt}

CONVERSATION CONTEXT:
{profile_context}

{length_instructions.get(response_length, length_instructions["adaptive"])}

PERSONALIZATION GUIDELINES:
- Reference their location ({user_profile.location or 'Ireland'}) when relevant
- Consider their relationship status and living situation
- If they have children, prioritize family-focused resources
- Match the tone to their expressed needs and concerns
- Build on information they've already shared

SURVIVOR STORY USAGE (TRAUMA-INFORMED):
- Stories included have been screened for trauma safety and appropriateness
- Use provided framing language (introduction, content notes, empowerment messages)
- Frame stories as "Many survivors describe similar experiences..." or "One person shared..."
- Never use real names - refer to "a survivor" or "someone who went through this"
- Highlight strength and resilience shown in the stories
- If recovery/hope stories are present, gently mention that "healing and recovery are possible"
- Balance information with validation - don't let stories overwhelm factual guidance
- Use stories to normalize the person's experience and reduce isolation
- Include any content warnings naturally in your response
- Always end with empowerment messaging when stories are used
- If multiple stories are provided, weave them together rather than presenting separately"""
        
        # Prepare the prompt
        prompt = f"""CONTEXT FROM IRISH DOMESTIC VIOLENCE ORGANIZATIONS:
{context}

USER QUESTION: {query}

CONVERSATION HISTORY: Based on our conversation, I know this person is in {user_profile.location or 'Ireland'}{', has children' if user_profile.has_children else ''}{', and is primarily concerned about ' + user_profile.primary_concern if user_profile.primary_concern else ''}.

INSTRUCTIONS: Provide a personalized, empathetic response using the context. Reference their specific situation when relevant and follow the response length guidelines."""
        
        # Set max_tokens based on response length
        max_tokens_map = {
            "brief": 200,      # ~150 words
            "adaptive": 400,   # ~300 words  
            "detailed": 800    # ~600 words
        }
        max_tokens = max_tokens_map.get(response_length, 400)
        
        try:
            if self.llm_provider in ["openai", "openrouter"]:
                response = self.openai_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": enhanced_system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=max_tokens
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
        
        # Check for crisis indicators first with detailed analysis
        crisis_info = self.get_detailed_crisis_info(query)
        
        if crisis_info["is_crisis"]:
            # High-risk/immediate danger - emergency response
            return {
                "response": self.get_crisis_response(),
                "is_crisis": True,
                "sources": [],
                "metadata": {
                    "crisis_detected": True,
                    "crisis_level": crisis_info["crisis_level"],
                    "confidence": crisis_info["confidence"],
                    "reasoning": crisis_info["reasoning"],
                    "triggered_by": crisis_info["triggered_by"]
                }
            }
        
        elif crisis_info["crisis_level"] == "moderate_risk" and crisis_info.get("immediate_action_needed", False):
            # Only return generic response for true moderate risk with immediate action needed
            return {
                "response": self.get_moderate_risk_response(),
                "is_crisis": False,
                "sources": [],
                "metadata": {
                    "moderate_risk_detected": True,
                    "crisis_level": crisis_info["crisis_level"],
                    "confidence": crisis_info["confidence"],
                    "reasoning": crisis_info["reasoning"],
                    "triggered_by": crisis_info["triggered_by"]
                }
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
    
    print("Irish Domestic Violence RAG Pipeline Demo")
    print("=" * 60)
    print("Note: This demo uses local models. For production, consider OpenAI/Claude for better responses.")
    print()
    
    # Initialize RAG pipeline
    try:
        rag = DomesticViolenceRAG(llm_provider="ollama", model_name="llama3.2")
        print(" RAG pipeline initialized with Ollama")
    except Exception as e:
        print(f" Could not initialize RAG pipeline: {e}")
        print(" Make sure you have Ollama installed and llama3.2 model downloaded")
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
        print(f"\n Query {i}: '{query}'")
        print("-" * 50)
        
        try:
            result = rag.process_query(query)
            
            if result['is_crisis']:
                print(" CRISIS DETECTED")
            
            print(f" Response:\n{result['response']}")
            
            if result['sources']:
                print(f"\n Sources ({len(result['sources'])}):")
                for j, source in enumerate(result['sources'][:3], 1):
                    print(f"  {j}. [{source['organization']}] {source['content_type']} "
                          f"(Relevance: {source['relevance']:.2f})")
            
        except Exception as e:
            print(f"Error processing query: {e}")
    
    print(f"\n" + "=" * 60)
    print(" RAG Pipeline Demo Complete")
    print(" Ready for integration with Open WebUI or other chat interfaces")

if __name__ == "__main__":
    demo_rag_pipeline()