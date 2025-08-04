#!/usr/bin/env python3

from typing import Dict, List, Any, Optional
from enum import Enum
import re

class NarrativeType(Enum):
    VALIDATION = "validation"      # Stories that validate the user's experience
    HOPE = "hope"                 # Recovery stories that inspire hope
    EDUCATION = "education"       # Stories that educate about abuse patterns
    SAFETY = "safety"            # Stories about safety planning and escape

class TraumaRisk(Enum):
    LOW = "low"           # Minimal risk of retraumatization
    MODERATE = "moderate" # Some elements that could be triggering
    HIGH = "high"         # Strong potential for retraumatization

class TraumaInformedDelivery:
    
    def __init__(self):
        # Trigger warning keywords that indicate high trauma risk
        self.high_trauma_keywords = [
            'rape', 'sexual assault', 'beaten', 'hospital', 'weapon', 'knife',
            'gun', 'choked', 'strangled', 'broken bones', 'blood', 'bruises',
            'unconscious', 'nearly died', 'threatened to kill', 'suicide attempt'
        ]
        
        # Moderate trauma keywords
        self.moderate_trauma_keywords = [
            'hit', 'slapped', 'pushed', 'grabbed', 'hurt', 'pain', 'scared',
            'afraid', 'crying', 'screaming', 'police', 'court', 'restraining order'
        ]
        
        # Hope and recovery indicators
        self.hope_keywords = [
            'safe now', 'got help', 'escaped', 'freedom', 'better life', 
            'healing', 'recovery', 'support', 'children safe', 'new start',
            'therapy helped', 'rebuilt my life', 'found peace', 'happy now'
        ]
        
        # Empowerment language
        self.empowerment_keywords = [
            'survived', 'strong', 'brave', 'courage', 'fought back',
            'took control', 'made a plan', 'saved myself', 'worth it',
            'deserved better', 'not my fault', 'believed in myself'
        ]
    
    def assess_trauma_risk(self, content: str) -> TraumaRisk:
        
        content_lower = content.lower()
        
        # Check for high trauma content
        high_trauma_count = sum(1 for keyword in self.high_trauma_keywords 
                               if keyword in content_lower)
        
        if high_trauma_count >= 2:
            return TraumaRisk.HIGH
        elif high_trauma_count >= 1:
            return TraumaRisk.MODERATE
        
        # Check for moderate trauma content
        moderate_trauma_count = sum(1 for keyword in self.moderate_trauma_keywords 
                                   if keyword in content_lower)
        
        if moderate_trauma_count >= 3:
            return TraumaRisk.MODERATE
        elif moderate_trauma_count >= 1:
            return TraumaRisk.LOW
        
        return TraumaRisk.LOW
    
    def identify_narrative_type(self, content: str, metadata: Dict[str, Any]) -> List[NarrativeType]:
        
        narrative_types = []
        content_lower = content.lower()
        
        # Check for hope/recovery narratives
        hope_count = sum(1 for keyword in self.hope_keywords if keyword in content_lower)
        empowerment_count = sum(1 for keyword in self.empowerment_keywords if keyword in content_lower)
        
        if hope_count >= 2 or empowerment_count >= 2 or metadata.get('has_hope_element', False):
            narrative_types.append(NarrativeType.HOPE)
        
        # Check for validation narratives (describes abuse patterns)
        abuse_types = metadata.get('abuse_types_str', '').lower()
        if abuse_types and any(abuse_type in content_lower for abuse_type in abuse_types.split(',')):
            narrative_types.append(NarrativeType.VALIDATION)
        
        # Check for educational narratives (explains patterns/dynamics)
        educational_indicators = ['realized', 'understood', 'pattern', 'cycle', 'control', 'manipulation']
        if sum(1 for indicator in educational_indicators if indicator in content_lower) >= 2:
            narrative_types.append(NarrativeType.EDUCATION)
        
        # Check for safety narratives
        safety_indicators = ['escaped', 'left', 'plan', 'safe place', 'refuge', 'police', 'court']
        if sum(1 for indicator in safety_indicators if indicator in content_lower) >= 2:
            narrative_types.append(NarrativeType.SAFETY)
        
        return narrative_types if narrative_types else [NarrativeType.VALIDATION]
    
    def create_trauma_informed_framing(self, content: str, metadata: Dict[str, Any], 
                                     user_context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        
        trauma_risk = self.assess_trauma_risk(content)
        narrative_types = self.identify_narrative_type(content, metadata)
        survivor_name = metadata.get('survivor_name', 'Anonymous')
        
        # Create appropriate framing based on context
        framing = {}
        
        # Content warning if needed
        if trauma_risk in [TraumaRisk.HIGH, TraumaRisk.MODERATE]:
            framing['content_warning'] = self._create_content_warning(trauma_risk)
        
        # Introduction that validates without overwhelming
        framing['introduction'] = self._create_introduction(narrative_types, trauma_risk)
        
        # Processed content with trauma-informed edits
        framing['processed_content'] = self._process_content_for_safety(content, trauma_risk)
        
        # Hopeful conclusion if appropriate
        if NarrativeType.HOPE in narrative_types:
            framing['hope_conclusion'] = self._create_hope_conclusion()
        
        # Empowerment framing
        framing['empowerment_message'] = self._create_empowerment_message(narrative_types)
        
        return framing
    
    def _create_content_warning(self, trauma_risk: TraumaRisk) -> str:
        
        if trauma_risk == TraumaRisk.HIGH:
            return ("**Content Note:** The following account describes serious abuse. "
                   "Please take care of yourself while reading. You can skip this section "
                   "if it feels overwhelming.")
        else:
            return ("**Content Note:** This account describes experiences of abuse. "
                   "Please read at your own pace.")
    
    def _create_introduction(self, narrative_types: List[NarrativeType], 
                           trauma_risk: TraumaRisk) -> str:
        
        if NarrativeType.HOPE in narrative_types:
            return ("Many survivors have found their way to safety and healing. "
                   "One person shared their experience:")
        elif NarrativeType.VALIDATION in narrative_types:
            return ("You're not alone in what you're experiencing. "
                   "Others have described similar situations:")
        elif NarrativeType.EDUCATION in narrative_types:
            return ("Understanding abuse patterns can be helpful. "
                   "One survivor reflected on their experience:")
        else:
            return "Someone who has been through this shared:"
    
    def _process_content_for_safety(self, content: str, trauma_risk: TraumaRisk) -> str:
        
        if trauma_risk == TraumaRisk.LOW:
            return content
        
        processed = content
        
        # Soften extremely graphic language
        graphic_replacements = {
            r'\bbrutally\s+': '',
            r'\bviolently\s+': '',
            r'\bsavagely\s+': '',
            r'\bblood\s+everywhere': 'was injured',
            r'\bbroken\s+bones': 'serious injuries',
            r'\bunconscious': 'badly hurt'
        }
        
        for pattern, replacement in graphic_replacements.items():
            processed = re.sub(pattern, replacement, processed, flags=re.IGNORECASE)
        
        # Add validation statements for high-trauma content
        if trauma_risk == TraumaRisk.HIGH:
            processed = processed + "\n\n*What happened to this person was serious abuse and was never their fault.*"
        
        return processed
    
    def _create_hope_conclusion(self) -> str:
        
        return ("Recovery and healing are possible. Every person's journey is different, "
               "but you deserve safety and support in finding your path forward.")
    
    def _create_empowerment_message(self, narrative_types: List[NarrativeType]) -> str:
        
        if NarrativeType.HOPE in narrative_types:
            return "You have the strength to build a life free from abuse."
        elif NarrativeType.SAFETY in narrative_types:
            return "You know your situation best. Trust your instincts about your safety."
        elif NarrativeType.VALIDATION in narrative_types:
            return "Your experiences are valid, and you deserve to be believed and supported."
        else:
            return "You are not alone, and what you're experiencing is not your fault."
    
    def validate_story_delivery(self, story_data: Dict[str, Any], 
                               user_vulnerability: str = "unknown") -> Dict[str, Any]:
        
        content = story_data.get('content', '')
        metadata = story_data.get('metadata', {})
        
        trauma_risk = self.assess_trauma_risk(content)
        narrative_types = self.identify_narrative_type(content, metadata)
        
        # Determine if story should be delivered
        should_deliver = True
        modifications_needed = []
        
        # High-trauma content needs careful consideration
        if trauma_risk == TraumaRisk.HIGH:
            if user_vulnerability == "high" or user_vulnerability == "crisis":
                should_deliver = False
                modifications_needed.append("Content too triggering for current user state")
            else:
                modifications_needed.append("Requires content warning and processing")
        
        # Create delivery recommendations
        delivery_recommendations = {
            "should_deliver": should_deliver,
            "trauma_risk": trauma_risk.value,
            "narrative_types": [nt.value for nt in narrative_types],
            "modifications_needed": modifications_needed,
            "framing": self.create_trauma_informed_framing(content, metadata) if should_deliver else None
        }
        
        return delivery_recommendations

def create_trauma_informed_guidelines() -> Dict[str, Any]:
    
    guidelines = {
        "core_principles": [
            "Safety first - both physical and emotional safety",
            "Choice and control - users decide what to read/skip",
            "Trustworthiness and transparency - clear about story sources",
            "Collaboration - user-centered approach",
            "Empowerment - focus on strength and resilience",
            "Cultural considerations - respect diverse experiences"
        ],
        
        "content_delivery_rules": {
            "high_trauma_content": [
                "Always include content warnings",
                "Process language to reduce graphic details", 
                "Include validation statements",
                "Provide clear exit options",
                "Follow with support resources"
            ],
            
            "hope_stories": [
                "Frame as possibility, not expectation",
                "Acknowledge that healing takes time",
                "Avoid prescriptive language",
                "Include diverse pathways to recovery"
            ],
            
            "validation_stories": [
                "Emphasize patterns rather than specific details",
                "Use normalizing language",
                "Avoid comparing experiences",
                "Focus on shared humanity"
            ]
        },
        
        "language_guidelines": {
            "do_use": [
                "Person-first language (survivor, not victim)",
                "Strength-based framing",
                "Non-judgmental tone",
                "Validating statements",
                "Hope without pressure"
            ],
            
            "avoid": [
                "Graphic violence descriptions",
                "Victim-blaming language",
                "Prescriptive advice",
                "Comparisons between experiences",
                "False urgency or pressure"
            ]
        },
        
        "user_state_considerations": {
            "crisis": "No survivor stories - focus on immediate safety",
            "high_vulnerability": "Only low-trauma hope stories with extensive framing",
            "moderate_vulnerability": "Carefully framed validation and hope stories",
            "low_vulnerability": "Full range with appropriate framing",
            "information_seeking": "Educational narratives with context"
        }
    }
    
    return guidelines

if __name__ == "__main__":
    # Demo the trauma-informed delivery system
    print("🛡️ Trauma-Informed Narrative Delivery System")
    print("=" * 55)
    
    delivery_system = TraumaInformedDelivery()
    
    # Test sample content
    sample_story = {
        'content': """I was married for 8 years and he controlled everything. He would hit me when I tried to speak up and told me I was worthless. I finally got help from NCDV and escaped to safety. Now I have a new life and my children are safe. There is hope - you can get through this.""",
        'metadata': {
            'survivor_name': 'Anna',
            'abuse_types_str': 'physical, emotional, financial',
            'has_hope_element': True
        }
    }
    
    # Assess the story
    trauma_risk = delivery_system.assess_trauma_risk(sample_story['content'])
    narrative_types = delivery_system.identify_narrative_type(sample_story['content'], sample_story['metadata'])
    
    print(f"📊 Analysis Results:")
    print(f"   Trauma Risk: {trauma_risk.value}")
    print(f"   Narrative Types: {[nt.value for nt in narrative_types]}")
    
    # Create trauma-informed framing
    framing = delivery_system.create_trauma_informed_framing(
        sample_story['content'], sample_story['metadata']
    )
    
    print(f"\n📝 Trauma-Informed Framing:")
    for key, value in framing.items():
        print(f"   {key}: {value}")
    
    # Validate delivery
    validation = delivery_system.validate_story_delivery(sample_story, "moderate_vulnerability")
    
    print(f"\n✅ Delivery Validation:")
    print(f"   Should Deliver: {validation['should_deliver']}")
    print(f"   Modifications: {validation['modifications_needed']}")
    
    print(f"\n📋 Guidelines created - ready for integration with RAG pipeline")