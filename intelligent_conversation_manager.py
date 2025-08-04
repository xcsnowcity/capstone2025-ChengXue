#!/usr/bin/env python3

import json
import os
import re
from typing import Dict, List, Any, Optional
from dataclasses import asdict
from dotenv import load_dotenv

# Import existing conversation flow components
from conversation_flow import UserProfile, SafetyLevel, ConversationStage

# LLM imports
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# Load environment variables
load_dotenv()

class IntelligentConversationManager:
    def __init__(self, 
                 llm_provider: str = "openrouter",
                 model_name: str = "anthropic/claude-3.5-haiku",
                 temperature: float = 0.3):
        
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
        else:
            raise ValueError(f"LLM provider '{llm_provider}' not available or not installed")
        
        # Crisis keywords for immediate detection
        self.crisis_keywords = [
            "kill myself", "want to die", "end it all", "suicide", "suicidal",
            "can't go on", "no way out", "better off dead", "want to end it",
            "threatening me now", "has a weapon", "going to hurt me", "going to kill me",
            "immediate danger", "in danger right now", "he's here", "she's here", 
            "scared for my life", "emergency", "help me now", "has a knife", "has a gun"
        ]
        
        # RAG trigger phrases for specific information requests
        self.rag_trigger_phrases = [
            "what counts as", "is this abuse", "what are my rights", "how do i get",
            "what support is available", "what services", "legal rights", "safety order",
            "protection order", "barring order", "what is", "definition of", "types of abuse",
            "financial abuse", "emotional abuse", "coercive control", "domestic violence act"
        ]
        
        # Response length indicators
        self.brief_indicators = [
            "quickly", "brief", "summary", "short answer", "simple explanation",
            "in short", "just tell me", "quick question", "overview"
        ]
        
        self.detailed_indicators = [
            "detailed", "comprehensive", "full information", "everything about",
            "complete guide", "step by step", "all details", "thorough"
        ]
    
    def get_conversation_prompt(self) -> str:
        return """You are a compassionate conversation manager for a domestic violence support chatbot in Ireland.

CRITICAL ROLE: You handle the initial conversation phase before users get specific information from the knowledge base.

YOUR RESPONSIBILITIES:
1. Have natural, empathetic conversations with users who may be in vulnerable situations
2. Organically gather key profile information through conversation (NOT interrogation)
3. Decide when the user is ready for specific information (RAG pipeline) vs needs continued support
4. ALWAYS prioritize safety - detect crisis situations immediately

PROFILE INFORMATION TO GATHER NATURALLY:
- safety_level: immediate_danger, high_risk, moderate_risk, low_risk, unknown
- location: Irish county name (dublin, cork, galway, etc.)
- relationship_status: married, dating, separated, single
- has_children: true/false
- housing_situation: cohabiting, separated, independent
- primary_concern: legal_information, safety_planning, emotional_support, practical_resources

DECISION MAKING:
- USE_RAG when: User asks specific questions about laws, procedures, services, "how do I...", "what are my rights...", "what counts as...", "is [specific thing] abuse?", "what support is available in [location]", definitions of abuse types, local services
- CONTINUE_CONVERSATION when: User is sharing their story, needs emotional support, is still processing, asks very general questions, expressing feelings without seeking specific information
- CRISIS_MODE when: Immediate danger, suicide ideation, threats, weapons mentioned, "want to die", "kill myself", "end it all"

IRISH CONTEXT:
- Reference Irish law (Domestic Violence Act 2018)
- Mention Irish organizations: Women's Aid (1800 341 900), Safe Ireland, local services
- Understand Irish counties and legal system

CONVERSATION STYLE:
- Trauma-informed: validate feelings, never blame, use gentle language
- Empathetic but professional
- Ask open-ended questions naturally
- Don't rush to gather all information at once
- Let users share at their own pace

RESPONSE FORMAT: Always respond with ONLY valid JSON, no other text:
{
    "response": "Your empathetic response to the user",
    "action": "continue_conversation|use_rag|crisis_mode",
    "profile_updates": {
        "field_name": "new_value"
    },
    "confidence": 0.8,
    "reasoning": "Brief explanation of your decision"
}

IMPORTANT: Return ONLY the JSON object above, no explanatory text before or after.

SAFETY NOTES:
- If ANY crisis keywords detected, immediately choose "crisis_mode"
- If user seems overwhelmed, slow down information gathering
- Always validate their experience and feelings
- Remind about confidentiality and quick exit options when appropriate"""

    def detect_immediate_crisis(self, message: str) -> bool:
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in self.crisis_keywords)
    
    def detect_rag_triggers(self, message: str) -> bool:
        message_lower = message.lower()
        return any(phrase in message_lower for phrase in self.rag_trigger_phrases)
    
    def detect_response_length_preference(self, message: str) -> str:
        message_lower = message.lower()
        
        if any(indicator in message_lower for indicator in self.brief_indicators):
            return "brief"
        elif any(indicator in message_lower for indicator in self.detailed_indicators):
            return "detailed"
        else:
            return "adaptive"  # Default: adaptive based on context
    
    def build_conversation_context(self, 
                                 user_profile: UserProfile, 
                                 conversation_history: List[Dict[str, str]]) -> str:
        # Profile context
        profile_info = []
        if user_profile.safety_level != SafetyLevel.UNKNOWN:
            profile_info.append(f"Safety level: {user_profile.safety_level.value}")
        if user_profile.location:
            profile_info.append(f"Location: {user_profile.location}")
        if user_profile.relationship_status:
            profile_info.append(f"Relationship: {user_profile.relationship_status}")
        if user_profile.has_children is not None:
            profile_info.append(f"Has children: {user_profile.has_children}")
        if user_profile.primary_concern:
            profile_info.append(f"Primary concern: {user_profile.primary_concern}")
        
        profile_context = "Current profile: " + ("; ".join(profile_info) if profile_info else "No information gathered yet")
        
        # Conversation history context
        if conversation_history:
            recent_exchanges = conversation_history[-3:]  # Last 3 exchanges
            history_context = "Recent conversation:\n"
            for exchange in recent_exchanges:
                history_context += f"User: {exchange.get('user', 'N/A')}\n"
                history_context += f"Bot: {exchange.get('bot', 'N/A')}\n"
        else:
            history_context = "Recent conversation: This is the start of the conversation"
        
        return f"{profile_context}\n\n{history_context}"
    
    def process_message(self, 
                       message: str, 
                       user_profile: UserProfile,
                       conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
        if conversation_history is None:
            conversation_history = []
        
        # Quick crisis detection
        if self.detect_immediate_crisis(message):
            return {
                "response": self.get_crisis_response(),
                "action": "crisis_mode",
                "profile_updates": {"safety_level": "immediate_danger"},
                "confidence": 1.0,
                "reasoning": "Crisis keywords detected in user message",
                "safety_triggered": True
            }
        
        # Quick RAG trigger detection
        if self.detect_rag_triggers(message):
            response_length = self.detect_response_length_preference(message)
            return {
                "response": "I understand you're looking for specific information. Let me help you with that.",
                "action": "use_rag",
                "profile_updates": {"primary_concern": "information_seeking"},
                "confidence": 0.9,
                "reasoning": "User asked specific question that requires knowledge base information",
                "safety_triggered": False,
                "response_length": response_length
            }
        
        # Build context for LLM
        context = self.build_conversation_context(user_profile, conversation_history)
        
        # Prepare LLM prompt
        prompt = f"""{self.get_conversation_prompt()}

CONTEXT:
{context}

USER MESSAGE: "{message}"

Analyze this message and respond with your decision in the required JSON format. Consider:
1. Is this a crisis situation requiring immediate help?
2. Is the user asking for specific information that needs the knowledge base?
3. Or do they need continued conversational support?

Remember: Be empathetic, gather information naturally, and prioritize safety."""

        try:
            # Get LLM response
            response = self.llm_client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=self.temperature,
                max_tokens=800
            )
            
            # Parse JSON response
            llm_output = response.choices[0].message.content.strip()
            
            # More robust JSON extraction
            decision = self._extract_json_from_response(llm_output)
            
            # Validate required fields
            required_fields = ["response", "action", "profile_updates"]
            for field in required_fields:
                if field not in decision:
                    decision[field] = {} if field == "profile_updates" else ""
            
            # Add safety flag
            decision["safety_triggered"] = decision.get("action") == "crisis_mode"
            
            # Ensure confidence is set
            if "confidence" not in decision:
                decision["confidence"] = 0.7
            
            return decision
            
        except json.JSONDecodeError as e:
            # Fallback if JSON parsing fails
            return {
                "response": """I understand you're reaching out for support, and I want to help you. 
                
Can you tell me a bit more about what's on your mind today? I'm here to listen and provide information that might be helpful for your situation.

Remember, this conversation is confidential and you can use the Quick Exit button anytime if needed.""",
                "action": "continue_conversation",
                "profile_updates": {},
                "confidence": 0.5,
                "reasoning": f"JSON parsing error: {str(e)}, using fallback response",
                "safety_triggered": False
            }
            
        except Exception as e:
            # General error fallback
            return {
                "response": """I'm here to support you, though I'm having a small technical issue right now. 

For immediate help, you can always contact:
- **Women's Aid 24/7 Helpline: 1800 341 900** (free, confidential)
- **Emergency: 999 or 112**

Can you tell me what you'd like help with today?""",
                "action": "continue_conversation",
                "profile_updates": {},
                "confidence": 0.3,
                "reasoning": f"Technical error: {str(e)}",
                "safety_triggered": False
            }
    
    def _extract_json_from_response(self, llm_output: str) -> Dict[str, Any]:
        """Extract JSON from LLM response with multiple fallback strategies."""
        
        # Strategy 1: Try direct JSON parsing
        try:
            return json.loads(llm_output)
        except json.JSONDecodeError:
            pass
        
        # Strategy 2: Extract from code blocks
        
        # Look for ```json blocks
        json_match = re.search(r'```json\s*\n(.*?)\n```', llm_output, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Look for ``` blocks (without json)
        code_match = re.search(r'```\s*\n(.*?)\n```', llm_output, re.DOTALL)
        if code_match:
            try:
                return json.loads(code_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Strategy 3: Find JSON within text
        # Look for { ... } patterns
        brace_match = re.search(r'\{.*\}', llm_output, re.DOTALL)
        if brace_match:
            try:
                return json.loads(brace_match.group(0))
            except json.JSONDecodeError:
                pass
        
        # Strategy 4: Manual parsing for common patterns
        # If LLM provides a structured response, try to parse key fields
        response_text = ""
        action = "continue_conversation"
        profile_updates = {}
        
        # Extract response text (look for common patterns)
        if "response" in llm_output.lower():
            response_patterns = [
                r'"response":\s*"([^"]*)"',
                r"response:\s*(.+?)(?:\n|$)",
                r"Response:\s*(.+?)(?:\n|$)"
            ]
            for pattern in response_patterns:
                match = re.search(pattern, llm_output, re.IGNORECASE)
                if match:
                    response_text = match.group(1).strip()
                    break
        
        # Extract action
        if "use_rag" in llm_output.lower():
            action = "use_rag"
        elif "crisis" in llm_output.lower():
            action = "crisis_mode"
        
        # If we got some response text, use it
        if response_text:
            return {
                "response": response_text,
                "action": action,
                "profile_updates": profile_updates,
                "confidence": 0.6,
                "reasoning": "Parsed from structured text (not JSON)"
            }
        
        # Strategy 5: Complete fallback - raise error to trigger fallback response
        raise json.JSONDecodeError("Could not extract JSON from response", llm_output, 0)

    def get_crisis_response(self) -> str:
        """Return immediate crisis response."""
        return """🚨 **IMMEDIATE HELP NEEDED**

I'm very concerned about your safety. Please:

**Call 999 or 112 immediately** if you're in immediate danger
**Women's Aid 24/7 Helpline: 1800 341 900** (free, confidential)
**Text "Hi" to 50818** for instant message support

If you can't call:
- Go to your nearest Garda station
- Go to a public place with people around
- Contact a trusted friend or family member

**Quick Exit** button is available if you need to leave this conversation quickly.

You don't have to face this alone. Help is available right now."""
    
    def update_user_profile(self, 
                           user_profile: UserProfile, 
                           profile_updates: Dict[str, Any]) -> UserProfile:
        
        for field, value in profile_updates.items():
            if hasattr(user_profile, field):
                # Handle safety level enum conversion
                if field == "safety_level" and isinstance(value, str):
                    try:
                        setattr(user_profile, field, SafetyLevel(value))
                    except ValueError:
                        # If invalid enum value, keep existing
                        pass
                else:
                    setattr(user_profile, field, value)
        
        return user_profile


def demo_intelligent_conversation():
    
    print("🤖 Intelligent Conversation Manager Demo")
    print("=" * 50)
    print("This simulates the conversation management phase before RAG pipeline")
    print()
    
    try:
        # Initialize conversation manager
        manager = IntelligentConversationManager(
            llm_provider="openrouter",
            model_name="anthropic/claude-3.5-haiku"
        )
        print("✅ Intelligent Conversation Manager initialized")
        
        # Create sample user profile
        user_profile = UserProfile(session_id="demo_session")
        conversation_history = []
        
        # Test scenarios
        test_messages = [
            "Hi, I think I need help but I'm not sure where to start",
            "My partner has been getting really angry lately and I'm scared",
            "I want to kill myself, I can't take this anymore",  # Crisis test
            "What are my legal rights if I'm married?",  # RAG trigger
            "I have two young children and I'm worried about them"
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n🔍 Test {i}: '{message}'")
            print("-" * 40)
            
            try:
                result = manager.process_message(message, user_profile, conversation_history)
                
                print(f"📝 Response: {result['response'][:150]}...")
                print(f"🎯 Action: {result['action']}")
                print(f"📊 Profile Updates: {result['profile_updates']}")
                print(f"🔍 Reasoning: {result['reasoning']}")
                print(f"⚠️  Crisis Detected: {result['safety_triggered']}")
                
                # Update profile for next iteration
                if result['profile_updates']:
                    user_profile = manager.update_user_profile(user_profile, result['profile_updates'])
                
                # Add to conversation history
                conversation_history.append({
                    'user': message,
                    'bot': result['response']
                })
                
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print(f"\n" + "=" * 50)
        print("✅ Demo Complete - Ready for integration!")
        
    except Exception as e:
        print(f"❌ Could not initialize: {e}")
        print("💡 Make sure you have OPENROUTER_API_KEY set in your .env file")


if __name__ == "__main__":
    demo_intelligent_conversation()