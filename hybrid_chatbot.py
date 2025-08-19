#!/usr/bin/env python3
import os
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Import existing components
from rag_pipeline import DomesticViolenceRAG
from llm_crisis_detector import LLMCrisisDetector, CrisisLevel
from trauma_informed_delivery import TraumaInformedDelivery

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

@dataclass
class ConversationContext:
    # Track conversation state and triggers
    user_location: Optional[str] = None
    mentioned_abuse_types: List[str] = None
    expressed_needs: List[str] = None
    safety_concerns: List[str] = None
    has_children: Optional[bool] = None
    message_count: int = 0
    last_rag_trigger: Optional[int] = None
    crisis_level: Optional[str] = None
    
    def __post_init__(self):
        if self.mentioned_abuse_types is None:
            self.mentioned_abuse_types = []
        if self.expressed_needs is None:
            self.expressed_needs = []
        if self.safety_concerns is None:
            self.safety_concerns = []

class HybridDomesticViolenceChatbot:
    # Unified chatbot that seamlessly blends empathetic conversation with resource delivery

    def __init__(self, 
                 llm_provider: str = "openrouter",
                 model_name: str = "anthropic/claude-3.5-haiku",
                 temperature: float = 0.3):
        
        # Initialize core components
        self.rag_system = DomesticViolenceRAG(llm_provider, model_name, temperature=temperature)
        self.crisis_detector = LLMCrisisDetector(llm_provider, model_name)
        self.trauma_delivery = TraumaInformedDelivery()
        
        # LLM configuration
        self.llm_provider = llm_provider
        self.model_name = model_name
        self.temperature = temperature
        
        # Initialize LLM client
        if llm_provider == "openai" and OPENAI_AVAILABLE:
            self.llm_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif llm_provider == "openrouter" and OPENAI_AVAILABLE:
            self.llm_client = openai.OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENROUTER_API_KEY"),
            )
        elif llm_provider == "ollama" and OLLAMA_AVAILABLE:
            self.llm_client = ollama.Client()
        else:
            raise ValueError(f"LLM provider '{llm_provider}' not available")
        
        # Conversation state
        self.conversation_context = ConversationContext()
        self.conversation_history = []
        
        # Smart trigger keywords for automatic RAG activation
        self.location_triggers = [
            'dublin', 'cork', 'galway', 'limerick', 'waterford', 'derry', 'belfast',
            'kilkenny', 'wexford', 'carlow', 'laois', 'offaly', 'kildare', 'wicklow',
            'meath', 'louth', 'monaghan', 'cavan', 'longford', 'westmeath', 'roscommon',
            'sligo', 'leitrim', 'donegal', 'mayo', 'clare', 'tipperary', 'kerry'
        ]
        
        self.need_triggers = [
            'safe place', 'refuge', 'shelter', 'accommodation', 'somewhere to stay',
            'legal help', 'solicitor', 'lawyer', 'court', 'order', 'protection',
            'counselling', 'therapy', 'support group', 'financial help', 'money',
            'childcare', 'school', 'medical', 'doctor', 'hospital', 'police',
            'escape', 'leave', 'get out', 'safety plan', 'emergency bag',
            'what to pack', 'emergency kit', 'what should i pack', 'safety items',
            'prepare', 'planning', 'escape plan'
        ]
        
        self.abuse_indicators = [
            'hits', 'hit', 'punch', 'slap', 'hurt', 'hurts', 'violence', 'violent',
            'control', 'controls', 'controlling', 'monitor', 'monitors', 'isolate',
            'isolates', 'jealous', 'threats', 'threaten', 'scared', 'afraid',
            'coercive', 'manipulate', 'gaslight', 'financial abuse', 'emotional abuse'
        ]
    
    def analyze_message_context(self, message: str) -> Dict[str, Any]:
        # Analyze user message for triggers and context updates

        message_lower = message.lower()
        context_updates = {
            'rag_triggers': [],
            'location_detected': None,
            'needs_detected': [],
            'abuse_mentioned': [],
            'children_mentioned': False,
            'should_trigger_rag': False
        }
        
        # Detect location
        for location in self.location_triggers:
            if location in message_lower:
                context_updates['location_detected'] = location.title()
                context_updates['rag_triggers'].append(f"location:{location}")
                context_updates['should_trigger_rag'] = True
                break
        
        # Detect specific needs
        for need in self.need_triggers:
            if need in message_lower:
                context_updates['needs_detected'].append(need)
                context_updates['rag_triggers'].append(f"need:{need}")
                context_updates['should_trigger_rag'] = True
        
        # Detect abuse mentions
        for indicator in self.abuse_indicators:
            if indicator in message_lower:
                context_updates['abuse_mentioned'].append(indicator)
                context_updates['rag_triggers'].append(f"abuse:{indicator}")
        
        # Detect children
        children_keywords = ['child', 'children', 'kids', 'son', 'daughter', 'baby']
        if any(keyword in message_lower for keyword in children_keywords):
            context_updates['children_mentioned'] = True
        
        # Trigger RAG after multiple exchanges without resources
        if (self.conversation_context.message_count >= 3 and 
            (self.conversation_context.last_rag_trigger is None or 
             self.conversation_context.message_count - self.conversation_context.last_rag_trigger >= 3)):
            context_updates['should_trigger_rag'] = True
            context_updates['rag_triggers'].append("conversation_depth")
        
        return context_updates
    
    def is_information_seeking_query(self, message: str) -> bool:
        # Detect if message is seeking information rather than expressing crisis

        message_lower = message.lower()
        
        # Question indicators - likely seeking information
        question_indicators = [
            'what', 'how', 'where', 'when', 'why', 'which', 'who',
            'what should i', 'how do i', 'where can i', 'what if',
            'should i', 'can i', 'do i need', 'is it', 'are there'
        ]
        
        has_question_indicator = any(indicator in message_lower for indicator in question_indicators)
        
        # Safety planning keywords - not immediate crisis
        safety_planning_keywords = [
            'emergency bag', 'safety plan', 'what to pack', 'prepare',
            'planning', 'in case', 'if i need', 'safety kit',
            'escape plan', 'what should i pack', 'safety items'
        ]
        
        is_safety_planning = any(keyword in message_lower for keyword in safety_planning_keywords)
        
        # Information seeking about abuse/DV - not immediate crisis
        info_seeking_keywords = [
            'what is', 'definition of', 'explain', 'tell me about',
            'information about', 'learn about', 'understand',
            'difference between', 'types of', 'signs of'
        ]
        
        is_info_seeking = any(keyword in message_lower for keyword in info_seeking_keywords)
        
        # Legal/process questions - not immediate crisis
        legal_process_keywords = [
            'how to apply', 'application process', 'court process',
            'legal steps', 'procedure', 'requirements', 'documents needed'
        ]
        
        is_legal_process = any(keyword in message_lower for keyword in legal_process_keywords)
        
        # Future tense - planning rather than immediate crisis
        future_planning = any(phrase in message_lower for phrase in [
            'if i', 'when i', 'should i', 'planning to', 'thinking about',
            'in the future', 'eventually', 'someday'
        ])
        
        return (has_question_indicator or is_safety_planning or 
                is_info_seeking or is_legal_process or future_planning)
    
    def update_conversation_context(self, message: str, analysis: Dict[str, Any]):
        # Update conversation context with analysis results
        
        self.conversation_context.message_count += 1
        
        if analysis['location_detected']:
            self.conversation_context.user_location = analysis['location_detected']
        
        if analysis['needs_detected']:
            self.conversation_context.expressed_needs.extend(analysis['needs_detected'])
        
        if analysis['abuse_mentioned']:
            self.conversation_context.mentioned_abuse_types.extend(analysis['abuse_mentioned'])
        
        if analysis['children_mentioned']:
            self.conversation_context.has_children = True
        
        if analysis['should_trigger_rag']:
            self.conversation_context.last_rag_trigger = self.conversation_context.message_count
    
    def generate_hybrid_response(self, user_message: str) -> Dict[str, Any]:
        # Generate response that combines empathy with intelligent resource delivery

        # 1. Improved crisis detection - check for real crisis vs information seeking
        crisis_result = self.crisis_detector.detect_crisis_hybrid(user_message)
        
        # Don't trigger crisis for information-seeking questions
        is_information_seeking = self.is_information_seeking_query(user_message)
        
        if (crisis_result.crisis_level in [CrisisLevel.IMMEDIATE_DANGER, CrisisLevel.HIGH_RISK] and 
            not is_information_seeking):
            return {
                "response": self.rag_system.get_crisis_response(),
                "type": "crisis",
                "rag_used": False,
                "resources_provided": True,
                "crisis_level": crisis_result.crisis_level.value
            }
        
        # 2. Analyze message for context and triggers
        analysis = self.analyze_message_context(user_message)
        self.update_conversation_context(user_message, analysis)
        
        # 3. Build context-aware system prompt
        system_prompt = self.build_adaptive_system_prompt(analysis)
        
        # 4. Retrieve relevant resources if triggered
        relevant_resources = None
        if analysis['should_trigger_rag']:
            # Build RAG query from context
            rag_query = self.build_rag_query(user_message, analysis)
            rag_result = self.rag_system.process_query(rag_query)
            relevant_resources = rag_result
        
        # 5. Generate unified response
        response = self.generate_unified_response(
            user_message, 
            system_prompt, 
            relevant_resources,
            analysis
        )
        
        # 6. Add to conversation history
        self.conversation_history.append({
            "user_message": user_message,
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "context": self.conversation_context.__dict__.copy(),
            "analysis": analysis
        })
        
        return {
            "response": response,
            "type": "hybrid",
            "rag_used": relevant_resources is not None,
            "resources_provided": relevant_resources is not None,
            "context_triggers": analysis['rag_triggers'],
            "conversation_context": self.conversation_context.__dict__
        }
    
    def build_adaptive_system_prompt(self, analysis: Dict[str, Any]) -> str:
        #Build system prompt that adapts to conversation context
        
        base_prompt = """You are a compassionate AI assistant helping survivors of domestic violence in Ireland. 

CORE PRINCIPLES:
- Be warm, empathetic, and validating
- Use trauma-informed language (no victim-blaming)
- Acknowledge their courage in reaching out
- Provide specific, actionable Irish resources when relevant
- Balance emotional support with practical help
- Always include safety reminders

CONVERSATION CONTEXT:"""
        
        # Add known context
        context_parts = []
        if self.conversation_context.user_location:
            context_parts.append(f"Location: {self.conversation_context.user_location}")
        
        if self.conversation_context.has_children:
            context_parts.append("Has children - prioritize family safety resources")
        
        if self.conversation_context.expressed_needs:
            context_parts.append(f"Expressed needs: {', '.join(self.conversation_context.expressed_needs)}")
        
        if self.conversation_context.mentioned_abuse_types:
            context_parts.append(f"Mentioned experiences: {', '.join(set(self.conversation_context.mentioned_abuse_types))}")
        
        if context_parts:
            base_prompt += "\n" + "\n".join(f"- {part}" for part in context_parts)
        
        # Add response guidance based on triggers
        if analysis['should_trigger_rag']:
            base_prompt += """

RESOURCE DELIVERY MODE:
- Include specific Irish organizations and contact details
- Provide clear, actionable next steps
- Use the provided resource information to give concrete help
- Balance resources with empathetic acknowledgment
"""
        else:
            base_prompt += """

CONVERSATION MODE:
- Focus on empathetic listening and validation
- Gently gather context if helpful
- Offer general support and encouragement
- Let them guide the conversation pace
"""
        
        base_prompt += """

SAFETY REMINDERS:
- Always include Women's Aid helpline: 1800 341 900
- Emergency services: 999/112 for immediate danger
- Remind about browser history clearing if needed

TONE: Warm, professional, hopeful, non-judgmental"""
        
        return base_prompt
    
    def build_rag_query(self, user_message: str, analysis: Dict[str, Any]) -> str:
        #Build optimized query for RAG system based on context
        
        query_parts = []
        
        # Include location if detected
        if analysis['location_detected']:
            query_parts.append(f"support services in {analysis['location_detected']}")
        elif self.conversation_context.user_location:
            query_parts.append(f"support services in {self.conversation_context.user_location}")
        
        # Include specific needs
        if analysis['needs_detected']:
            query_parts.extend(analysis['needs_detected'])
        
        # Include abuse types for relevant resources
        if analysis['abuse_mentioned']:
            query_parts.extend(analysis['abuse_mentioned'])
        
        # Add children focus if relevant
        if self.conversation_context.has_children:
            query_parts.append("family support children safety")
        
        # Fall back to original message if no specific triggers
        if not query_parts:
            query_parts = [user_message]
        
        return " ".join(query_parts)
    
    def generate_unified_response(self, 
                                user_message: str, 
                                system_prompt: str,
                                relevant_resources: Optional[Dict],
                                analysis: Dict[str, Any]) -> str:
        # Generate unified response combining empathy with resources
        
        # Build user prompt
        user_prompt = f"User message: {user_message}"
        
        # Add resource context if available
        if relevant_resources and relevant_resources.get('sources'):
            resource_context = f"""

RELEVANT IRISH RESOURCES TO INCLUDE:
{self.format_resources_for_prompt(relevant_resources)}

INSTRUCTIONS: Integrate these specific resources naturally into your empathetic response."""
            user_prompt += resource_context
        
        # Add conversation history context
        if len(self.conversation_history) > 0:
            recent_context = f"""

RECENT CONVERSATION:
{self.format_conversation_context()}"""
            user_prompt += recent_context
        
        try:
            if self.llm_provider in ["openai", "openrouter"]:
                response = self.llm_client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=self.temperature,
                    max_tokens=600
                )
                return response.choices[0].message.content
            
            elif self.llm_provider == "ollama":
                response = self.llm_client.chat(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    options={"temperature": self.temperature}
                )
                return response['message']['content']
                
        except Exception as e:
            return f"I'm having trouble responding right now, but I want you to know that help is available. Please contact Women's Aid at 1800 341 900 for immediate support. Your safety matters."
    
    def format_resources_for_prompt(self, rag_result: Dict) -> str:
        # Format RAG results for inclusion in LLM prompt

        if not rag_result.get('sources'):
            return "No specific resources found."
        
        formatted = []
        for source in rag_result['sources'][:3]:  # Top 3 sources
            org = source.get('organization', 'Unknown')
            content_type = source.get('content_type', 'information')
            formatted.append(f"- {org} ({content_type}): Relevant support services available")
        
        # Include key response content if available
        if rag_result.get('response') and len(rag_result['response']) > 100:
            formatted.append(f"\nKey information: {rag_result['response'][:500]}...")
        
        return "\n".join(formatted)
    
    def format_conversation_context(self) -> str:
        # Format recent conversation for context

        if not self.conversation_history:
            return "First message in conversation"
        
        recent = self.conversation_history[-2:]  # Last 2 exchanges
        formatted = []
        
        for exchange in recent:
            formatted.append(f"User: {exchange['user_message'][:100]}...")
            formatted.append(f"Assistant: {exchange['response'][:100]}...")
        
        return "\n".join(formatted)
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        # Get summary of conversation state for debugging/analysis

        return {
            "context": self.conversation_context.__dict__,
            "message_count": len(self.conversation_history),
            "rag_triggers_used": sum(1 for msg in self.conversation_history if msg.get('analysis', {}).get('should_trigger_rag', False)),
            "resources_provided": sum(1 for msg in self.conversation_history if 'resources' in msg.get('response', '').lower()),
            "last_analysis": self.conversation_history[-1].get('analysis', {}) if self.conversation_history else {}
        }

def demo_hybrid_chatbot():
    # Demo the new hybrid chatbot design

    print("Hybrid Domestic Violence Support Chatbot Demo")
    print("=" * 50)
    
    try:
        chatbot = HybridDomesticViolenceChatbot(
            llm_provider="openrouter",
            model_name="anthropic/claude-3.5-haiku"
        )
        print("Hybrid chatbot initialized")
    except Exception as e:
        print(f"Failed to initialize: {e}")
        return
    
    # Test conversation from your example
    test_messages = [
        "who are you",
        "I want to find a safe place for me and my children",
        "like I said, I'm a mother and I want to find a safe place for me and my children in Galway.",
        "my husband. he keeps abuse us"
    ]
    
    print("\nTest Conversation:")
    print("=" * 30)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n[{i}] User: {message}")
        print("-" * 20)
        
        try:
            result = chatbot.generate_hybrid_response(message)
            
            print(f"Response: {result['response'][:300]}{'...' if len(result['response']) > 300 else ''}")
            print(f"Type: {result['type']} | RAG Used: {result['rag_used']} | Resources: {result['resources_provided']}")
            
            if result.get('context_triggers'):
                print(f"Triggers: {', '.join(result['context_triggers'])}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    # Show conversation summary
    print(f"\nConversation Summary:")
    summary = chatbot.get_conversation_summary()
    print(f"- Messages: {summary['message_count']}")
    print(f"- RAG Triggers: {summary['rag_triggers_used']}")
    print(f"- Resources Provided: {summary['resources_provided']}")
    print(f"- Final Context: {summary['context']}")

if __name__ == "__main__":
    demo_hybrid_chatbot()