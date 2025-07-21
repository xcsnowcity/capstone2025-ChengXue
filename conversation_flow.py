#!/usr/bin/env python3
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ConversationStage(Enum):
    """Stages of conversation flow"""
    GREETING = "greeting"
    SAFETY_CHECK = "safety_check"
    SITUATION_ASSESSMENT = "situation_assessment"
    SUPPORT_EXPLORATION = "support_exploration"
    RESOURCE_PROVISION = "resource_provision"
    ONGOING_SUPPORT = "ongoing_support"

class SafetyLevel(Enum):
    """Safety assessment levels"""
    IMMEDIATE_DANGER = "immediate_danger"
    HIGH_RISK = "high_risk"
    MODERATE_RISK = "moderate_risk"
    LOW_RISK = "low_risk"
    UNKNOWN = "unknown"

@dataclass
class UserProfile:
    """User profile built through conversation"""
    session_id: str
    safety_level: SafetyLevel = SafetyLevel.UNKNOWN
    location: Optional[str] = None
    county: Optional[str] = None
    relationship_status: Optional[str] = None
    has_children: Optional[bool] = None
    children_ages: List[str] = None
    employment_status: Optional[str] = None
    housing_situation: Optional[str] = None
    support_network: Optional[str] = None
    immigration_status: Optional[str] = None
    disability_status: Optional[str] = None
    primary_concern: Optional[str] = None
    help_seeking_history: Optional[str] = None
    readiness_level: Optional[str] = None
    preferred_contact: Optional[str] = None
    
    def __post_init__(self):
        if self.children_ages is None:
            self.children_ages = []

class ConversationManager:
    """Manages conversation flow and user profile building"""
    
    def __init__(self):
        self.irish_counties = [
            "carlow", "cavan", "clare", "cork", "donegal", "dublin",
            "galway", "kerry", "kildare", "kilkenny", "laois", "leitrim",
            "limerick", "longford", "louth", "mayo", "meath", "monaghan",
            "offaly", "roscommon", "sligo", "tipperary", "waterford",
            "westmeath", "wexford", "wicklow"
        ]
        
        # Safety assessment keywords
        self.immediate_danger_keywords = [
            "kill myself", "want to die", "end it all", "suicide",
            "threatening me now", "has a weapon", "going to hurt me",
            "immediate danger", "in danger right now", "he's here", "she's here", "hiding",
            "scared for my life", "going to kill", "emergency"
        ]
        
        self.high_risk_keywords = [
            "escalating", "getting worse", "threatens to kill",
            "choked me", "strangled", "isolated", "controlling everything",
            "took my phone", "won't let me leave", "following me"
        ]
        
        # Conversation prompts for different stages
        self.conversation_prompts = {
            ConversationStage.GREETING: {
                "first_time": """Hello, I'm here to provide support and information about domestic violence in Ireland. 
                
I want you to know:
- This conversation is confidential and anonymous
- You can leave at any time using the Quick Exit button
- I'm here to listen and provide information, not to judge

How are you feeling right now?""",
                
                "returning": """Welcome back. I'm glad you felt comfortable returning. 
                
How have you been since we last talked?"""
            },
            
            ConversationStage.SAFETY_CHECK: {
                "initial": """I'm concerned about your safety. Can you tell me:
- Are you in a safe place right now?
- Is the person who hurt you nearby?""",
                
                "follow_up": """Thank you for sharing that with me. 
                
Just to make sure - do you have somewhere safe you can go if you need to leave quickly?"""
            },
            
            ConversationStage.SITUATION_ASSESSMENT: {
                "location": """To help me provide you with the most relevant local support services, could you tell me what county you're in? 
                
(This helps me find services close to you)""",
                
                "relationship": """Can you tell me about your living situation? For example:
- Are you married, in a relationship, or separated?
- Do you live together?
                
This helps me understand what legal options might be available to you.""",
                
                "children": """Do you have children? If so, I can provide information about services that support families.
                
(You don't have to share details if you're not comfortable)""",
                
                "support": """Do you have family or friends you can talk to about what's happening?
                
Sometimes people feel isolated, and that's completely normal."""
            },
            
            ConversationStage.SUPPORT_EXPLORATION: {
                "needs": """What kind of support are you looking for today? For example:
- Information about your rights and options
- Emotional support and validation
- Practical help with safety planning
- Information about local services
                
There's no wrong answer - I'm here to help with whatever you need.""",
                
                "barriers": """What's the biggest challenge you're facing right now in getting the help you need?
                
Many people face barriers like fear, finances, or not knowing where to start.""",
                
                "readiness": """Some people are just beginning to think about their situation, others are ready to take action. 
                
Where do you feel you are right now? There's no pressure either way."""
            }
        }
    
    def assess_safety_level(self, user_input: str) -> SafetyLevel:
        """Assess user safety level based on their responses"""
        user_input_lower = user_input.lower()
        
        if any(keyword in user_input_lower for keyword in self.immediate_danger_keywords):
            return SafetyLevel.IMMEDIATE_DANGER
        elif any(keyword in user_input_lower for keyword in self.high_risk_keywords):
            return SafetyLevel.HIGH_RISK
        elif any(word in user_input_lower for word in ["afraid", "scared", "worried", "unsafe"]):
            return SafetyLevel.MODERATE_RISK
        else:
            return SafetyLevel.LOW_RISK
    
    def extract_location(self, user_input: str) -> Optional[str]:
        """Extract Irish county from user input"""
        user_input_lower = user_input.lower()
        
        for county in self.irish_counties:
            if county in user_input_lower:
                return county.title()
        return None
    
    def extract_relationship_info(self, user_input: str) -> Dict[str, Any]:
        """Extract relationship information"""
        user_input_lower = user_input.lower()
        info = {}
        
        # Relationship status
        if any(word in user_input_lower for word in ["married", "wife", "husband", "spouse"]):
            info["relationship_status"] = "married"
        elif any(word in user_input_lower for word in ["boyfriend", "girlfriend", "partner"]):
            info["relationship_status"] = "dating"
        elif any(word in user_input_lower for word in ["ex", "separated", "divorced"]):
            info["relationship_status"] = "separated"
        
        # Living situation
        if any(word in user_input_lower for word in ["live together", "living together", "same house"]):
            info["housing_situation"] = "cohabiting"
        elif any(word in user_input_lower for word in ["moved out", "separate", "don't live"]):
            info["housing_situation"] = "separated"
        
        return info
    
    def extract_children_info(self, user_input: str) -> Dict[str, Any]:
        """Extract information about children"""
        user_input_lower = user_input.lower()
        info = {}
        
        if any(word in user_input_lower for word in ["no children", "no kids", "don't have children", "don't have kids"]):
            info["has_children"] = False
        elif any(word in user_input_lower for word in ["children", "kids", "child", "son", "daughter"]):
            info["has_children"] = True
            
            # Try to extract ages
            age_indicators = ["year", "old", "age", "teenage", "baby", "toddler"]
            if any(indicator in user_input_lower for indicator in age_indicators):
                info["children_ages"] = [user_input]  # Store full context for now
        
        return info
    
    def get_next_prompt(self, stage: ConversationStage, user_profile: UserProfile, 
                       last_response: str = "") -> Dict[str, Any]:
        """Get the next appropriate prompt based on conversation stage and user profile"""
        
        # Update profile based on last response
        if last_response:
            self.update_profile_from_response(user_profile, last_response, stage)
        
        # Determine next stage and prompt
        if stage == ConversationStage.GREETING:
            return {
                "stage": ConversationStage.SAFETY_CHECK,
                "prompt": self.conversation_prompts[ConversationStage.SAFETY_CHECK]["initial"],
                "prompt_type": "safety_assessment"
            }
        
        elif stage == ConversationStage.SAFETY_CHECK:
            if user_profile.safety_level == SafetyLevel.IMMEDIATE_DANGER:
                return {
                    "stage": ConversationStage.SAFETY_CHECK,
                    "prompt": self.get_crisis_response(),
                    "prompt_type": "crisis_response"
                }
            else:
                return {
                    "stage": ConversationStage.SITUATION_ASSESSMENT,
                    "prompt": self.conversation_prompts[ConversationStage.SITUATION_ASSESSMENT]["location"],
                    "prompt_type": "location_assessment"
                }
        
        elif stage == ConversationStage.SITUATION_ASSESSMENT:
            if not user_profile.location:
                return {
                    "stage": ConversationStage.SITUATION_ASSESSMENT,
                    "prompt": self.conversation_prompts[ConversationStage.SITUATION_ASSESSMENT]["location"],
                    "prompt_type": "location_assessment"
                }
            elif not user_profile.relationship_status:
                return {
                    "stage": ConversationStage.SITUATION_ASSESSMENT,
                    "prompt": self.conversation_prompts[ConversationStage.SITUATION_ASSESSMENT]["relationship"],
                    "prompt_type": "relationship_assessment"
                }
            elif user_profile.has_children is None:
                return {
                    "stage": ConversationStage.SITUATION_ASSESSMENT,
                    "prompt": self.conversation_prompts[ConversationStage.SITUATION_ASSESSMENT]["children"],
                    "prompt_type": "children_assessment"
                }
            else:
                return {
                    "stage": ConversationStage.SUPPORT_EXPLORATION,
                    "prompt": self.conversation_prompts[ConversationStage.SUPPORT_EXPLORATION]["needs"],
                    "prompt_type": "needs_assessment"
                }
        
        elif stage == ConversationStage.SUPPORT_EXPLORATION:
            if not user_profile.primary_concern:
                return {
                    "stage": ConversationStage.SUPPORT_EXPLORATION,
                    "prompt": self.conversation_prompts[ConversationStage.SUPPORT_EXPLORATION]["needs"],
                    "prompt_type": "needs_assessment"
                }
            else:
                # Move to ongoing support for specific queries
                return {
                    "stage": ConversationStage.ONGOING_SUPPORT,
                    "prompt": None,  # Signal to use RAG pipeline
                    "prompt_type": "general_query"
                }
        
        elif stage == ConversationStage.RESOURCE_PROVISION:
            # Users asking questions after initial resource provision
            return {
                "stage": ConversationStage.ONGOING_SUPPORT,
                "prompt": None,  # Signal to use RAG pipeline
                "prompt_type": "general_query"
            }
        
        # Default to ongoing support - treat as regular query
        return {
            "stage": ConversationStage.ONGOING_SUPPORT,
            "prompt": None,  # Signal to use RAG pipeline
            "prompt_type": "general_query"
        }
    
    def update_profile_from_response(self, profile: UserProfile, response: str, stage: ConversationStage):
        """Update user profile based on their response"""
        
        # Safety assessment
        if stage == ConversationStage.SAFETY_CHECK:
            profile.safety_level = self.assess_safety_level(response)
        
        # Location extraction
        location = self.extract_location(response)
        if location:
            profile.location = location
            profile.county = location.lower()
        
        # Relationship information
        relationship_info = self.extract_relationship_info(response)
        if relationship_info:
            profile.relationship_status = relationship_info.get("relationship_status")
            profile.housing_situation = relationship_info.get("housing_situation")
        
        # Children information
        children_info = self.extract_children_info(response)
        if children_info:
            profile.has_children = children_info.get("has_children")
            if children_info.get("children_ages"):
                profile.children_ages.extend(children_info["children_ages"])
        
        # Support needs (based on keywords in response)
        if stage == ConversationStage.SUPPORT_EXPLORATION:
            response_lower = response.lower()
            if any(word in response_lower for word in ["legal", "rights", "court", "order"]):
                profile.primary_concern = "legal_information"
            elif any(word in response_lower for word in ["safety", "plan", "leave", "escape"]):
                profile.primary_concern = "safety_planning"
            elif any(word in response_lower for word in ["support", "talk", "listen", "emotional"]):
                profile.primary_concern = "emotional_support"
            elif any(word in response_lower for word in ["services", "help", "local", "resources"]):
                profile.primary_concern = "practical_resources"
    
    def get_crisis_response(self) -> str:
        """Get immediate crisis response"""
        return """🚨 **IMMEDIATE HELP NEEDED**

I'm very concerned about your safety. Please:

**Call 999 or 112 immediately** if you're in immediate danger
**Women's Aid 24/7 Helpline: 1800 341 900** (free, confidential)
**Text "Hi" to 50818** for instant message support

If you can't call:
- Go to your nearest Garda station
- Go to a public place with people around
- Contact a trusted friend or family member

**Quick Exit** button is at the top of this page if you need to leave quickly.

You deserve to be safe. Help is available right now."""
    
    def generate_personalized_response(self, profile: UserProfile) -> str:
        """Generate personalized response based on user profile"""
        response_parts = []
        
        # Acknowledgment
        response_parts.append("Thank you for sharing that with me. Based on what you've told me, here are some resources that might be helpful:")
        
        # Location-specific resources
        if profile.location:
            response_parts.append(f"\n**Local Support in {profile.location}:**")
            response_parts.append(f"- I can provide information about domestic violence services specifically in {profile.location}")
        
        # Children-specific resources
        if profile.has_children:
            response_parts.append(f"\n**Support for Families:**")
            response_parts.append("- Services that support both you and your children")
            response_parts.append("- Information about custody and child protection")
        
        # Legal information based on relationship status
        if profile.relationship_status == "married":
            response_parts.append(f"\n**Legal Information:**")
            response_parts.append("- Your rights as a married person under Irish law")
            response_parts.append("- Information about judicial separation and divorce")
        elif profile.relationship_status in ["dating", "separated"]:
            response_parts.append(f"\n**Legal Information:**")
            response_parts.append("- Your rights in non-marital relationships")
            response_parts.append("- Information about domestic violence orders")
        
        # Always include emergency contacts
        response_parts.append(f"\n**Always Available:**")
        response_parts.append("- **Women's Aid 24/7 Helpline: 1800 341 900**")
        response_parts.append("- **Emergency: 999 or 112**")
        
        response_parts.append(f"\nWhat specific information would be most helpful for you right now?")
        
        return "\n".join(response_parts)
    
    def get_conversation_summary(self, profile: UserProfile) -> Dict[str, Any]:
        """Get summary of conversation for context"""
        return {
            "safety_level": profile.safety_level.value,
            "location": profile.location,
            "relationship_status": profile.relationship_status,
            "has_children": profile.has_children,
            "primary_concern": profile.primary_concern,
            "profile_completeness": self.calculate_profile_completeness(profile)
        }
    
    def calculate_profile_completeness(self, profile: UserProfile) -> float:
        """Calculate how complete the user profile is"""
        total_fields = 8  # Key fields we want to gather
        completed_fields = 0
        
        if profile.safety_level != SafetyLevel.UNKNOWN:
            completed_fields += 1
        if profile.location:
            completed_fields += 1
        if profile.relationship_status:
            completed_fields += 1
        if profile.has_children is not None:
            completed_fields += 1
        if profile.housing_situation:
            completed_fields += 1
        if profile.primary_concern:
            completed_fields += 1
        if profile.support_network:
            completed_fields += 1
        if profile.readiness_level:
            completed_fields += 1
        
        return completed_fields / total_fields