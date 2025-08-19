#!/usr/bin/env python3
import os
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
from dotenv import load_dotenv

# LLM imports
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

load_dotenv()

class CrisisLevel(Enum):
    """Crisis severity levels"""
    IMMEDIATE_DANGER = "immediate_danger"  # Life-threatening situation
    HIGH_RISK = "high_risk"              # Severe risk, needs urgent help
    MODERATE_RISK = "moderate_risk"      # Concerning, needs support
    LOW_RISK = "low_risk"               # General support needed
    NO_CRISIS = "no_crisis"             # No crisis indicators

@dataclass
class CrisisDetectionResult:
    # Result of crisis detection analysis
    crisis_level: CrisisLevel
    confidence: float  # 0.0 to 1.0
    reasoning: str
    triggered_by: str  # "keywords", "llm", "both"
    immediate_action_needed: bool
    recommended_response: str

class LLMCrisisDetector:
    # Advanced crisis detection using both keywords and LLM analysis

    def __init__(self, 
                 llm_provider: str = "openrouter",
                 model_name: str = "anthropic/claude-3.5-haiku",
                 enable_llm: bool = True):
        
        self.llm_provider = llm_provider
        self.model_name = model_name
        self.enable_llm = enable_llm
        
        # Initialize LLM client if available
        if enable_llm and OPENAI_AVAILABLE:
            if llm_provider == "openrouter":
                self.llm_client = openai.OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=os.getenv("OPENROUTER_API_KEY"),
                )
            elif llm_provider == "openai":
                self.llm_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            else:
                self.enable_llm = False
                print(f"Warning: LLM provider '{llm_provider}' not supported, falling back to keywords only")
        else:
            self.enable_llm = False
            print("Warning: LLM not available, using keywords only")
        
        # Enhanced keyword sets for different crisis levels
        self.immediate_danger_keywords = [
            # Suicide/self-harm (immediate)
            "kill myself", "want to die", "end it all", "suicide", "overdose",
            "going to hurt myself", "can't live anymore", "ready to die",
            
            # Immediate physical danger
            "threatening me now", "has a weapon", "going to hurt me", "going to kill me",
            "in immediate danger", "he's here now", "she's here now", "hiding from",
            "scared for my life", "about to hurt me", "emergency", "call 911", "call 999",
            
            # Active violence
            "hitting me now", "attacking me", "trapped"
        ]
        
        self.high_risk_keywords = [
            # Escalation patterns
            "getting worse", "escalating", "more violent", "threatens to kill",
            "said he'll kill me", "said she'll kill me", "getting angrier",
            
            # Severe abuse indicators  
            "choked me", "strangled me", "suffocated me", "broke my bones",
            "sent to hospital", "black eyes", "bruises everywhere",
            
            # Isolation and control
            "won't let me leave", "took my phone", "locked me in", "following me",
            "watching me", "controls everything", "can't see family", "isolated"
        ]
        
        self.moderate_risk_keywords = [
            # Fear and distress
            "afraid", "scared", "terrified", "worried", "unsafe", "frightened",
            "don't know what to do", "feeling trapped", "desperate",
            
            # Emotional distress
            "can't cope", "falling apart", "breaking down", "losing hope",
            "feel hopeless", "overwhelmed", "can't take it anymore"
        ]
        
        # LLM system prompt for crisis detection
        self.crisis_detection_prompt = """You are a crisis detection specialist for domestic violence survivors in Ireland. 

Your task is to analyze user messages and detect crisis situations that require immediate intervention.

CRISIS LEVELS:
- IMMEDIATE_DANGER: Life-threatening situation requiring emergency services (999/112)
- HIGH_RISK: Severe situation requiring urgent professional help
- MODERATE_RISK: Concerning situation needing support
- LOW_RISK: General support situation
- NO_CRISIS: No crisis indicators detected

DETECTION CRITERIA:

IMMEDIATE_DANGER indicators:
- Explicit suicidal ideation or self-harm intent
- Active threats of violence happening now
- Someone with weapons present
- Being physically attacked or trapped
- Unable to escape immediate danger

HIGH_RISK indicators:
- Recent escalation in violence
- Threats of murder/serious harm
- Strangulation/choking (high lethality predictor)
- Severe isolation and control
- Recent separation (high-risk period)

MODERATE_RISK indicators:
- Expressions of fear, desperation, hopelessness
- Feeling trapped or overwhelmed
- Emotional distress about abuse situation
- Seeking help but not in immediate danger

Consider context, tone, and subtle expressions that keywords might miss.

IMPORTANT:
- Irish context: Consider cultural expressions and Irish English patterns
- Trauma-informed: People may not directly state danger due to shame/fear
- False positives are better than false negatives for safety
- Look for implicit cries for help

IMPORTANT: Respond with ONLY a valid JSON object, no other text:

{
    "crisis_level": "IMMEDIATE_DANGER",
    "confidence": 0.95,
    "reasoning": "Brief explanation of why this level was chosen",
    "key_indicators": ["concerning phrase 1", "concerning phrase 2"],
    "immediate_action": true
}

Crisis levels must be exactly one of: IMMEDIATE_DANGER, HIGH_RISK, MODERATE_RISK, LOW_RISK, NO_CRISIS"""

    def detect_crisis_keywords(self, message: str) -> CrisisDetectionResult:
        # Fast keyword-based crisis detection
        message_lower = message.lower()
        
        # Check immediate danger keywords
        immediate_triggers = [kw for kw in self.immediate_danger_keywords if kw in message_lower]
        if immediate_triggers:
            return CrisisDetectionResult(
                crisis_level=CrisisLevel.IMMEDIATE_DANGER,
                confidence=0.95,
                reasoning=f"Immediate danger keywords detected: {', '.join(immediate_triggers[:2])}",
                triggered_by="keywords",
                immediate_action_needed=True,
                recommended_response="emergency_crisis"
            )
        
        # Check high risk keywords
        high_risk_triggers = [kw for kw in self.high_risk_keywords if kw in message_lower]
        if high_risk_triggers:
            return CrisisDetectionResult(
                crisis_level=CrisisLevel.HIGH_RISK,
                confidence=0.85,
                reasoning=f"High risk keywords detected: {', '.join(high_risk_triggers[:2])}",
                triggered_by="keywords",
                immediate_action_needed=True,
                recommended_response="urgent_crisis"
            )
        
        # Check moderate risk keywords
        moderate_triggers = [kw for kw in self.moderate_risk_keywords if kw in message_lower]
        if len(moderate_triggers) >= 2:  # Need multiple indicators
            return CrisisDetectionResult(
                crisis_level=CrisisLevel.MODERATE_RISK,
                confidence=0.75,
                reasoning=f"Multiple moderate risk indicators: {', '.join(moderate_triggers[:2])}",
                triggered_by="keywords",
                immediate_action_needed=False,
                recommended_response="supportive_crisis"
            )
        elif len(moderate_triggers) == 1:
            return CrisisDetectionResult(
                crisis_level=CrisisLevel.LOW_RISK,
                confidence=0.6,
                reasoning=f"Single risk indicator: {moderate_triggers[0]}",
                triggered_by="keywords",
                immediate_action_needed=False,
                recommended_response="general_support"
            )
        
        return CrisisDetectionResult(
            crisis_level=CrisisLevel.NO_CRISIS,
            confidence=0.9,
            reasoning="No crisis keywords detected",
            triggered_by="keywords",
            immediate_action_needed=False,
            recommended_response="normal"
        )
    
    def detect_crisis_llm(self, message: str) -> Optional[CrisisDetectionResult]:
        # LLM-based crisis detection for nuanced analysis
        if not self.enable_llm:
            return None
        
        try:
            response = self.llm_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self.crisis_detection_prompt},
                    {"role": "user", "content": f"Analyze this message: '{message}'"}
                ],
                temperature=0.1,  # Low temperature for consistent results
                max_tokens=300
            )
            
            # Parse JSON response
            result_text = response.choices[0].message.content.strip()
            if result_text.startswith('```json'):
                result_text = result_text.split('```json')[1].split('```')[0].strip()
            elif result_text.startswith('```'):
                result_text = result_text.split('```')[1].strip()
            
            # Clean up any extra text after JSON
            try:
                # Try to find JSON object boundaries
                start_idx = result_text.find('{')
                end_idx = result_text.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    result_text = result_text[start_idx:end_idx+1]
                result_data = json.loads(result_text)
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print(f"Raw response: {result_text[:200]}...")
                return None
            
            return CrisisDetectionResult(
                crisis_level=CrisisLevel(result_data["crisis_level"].lower()),
                confidence=result_data["confidence"],
                reasoning=result_data["reasoning"],
                triggered_by="llm",
                immediate_action_needed=result_data["immediate_action"],
                recommended_response=self._map_crisis_level_to_response(
                    CrisisLevel(result_data["crisis_level"].lower())
                )
            )
            
        except Exception as e:
            print(f"LLM crisis detection error: {e}")
            return None
    
    def detect_crisis_hybrid(self, message: str) -> CrisisDetectionResult:
        # Hybrid crisis detection combining keywords and LLM
        
        # Always run keyword detection first (fast and reliable)
        keyword_result = self.detect_crisis_keywords(message)
        
        # If keywords detect immediate danger, don't wait for LLM
        if keyword_result.crisis_level == CrisisLevel.IMMEDIATE_DANGER:
            return keyword_result
        
        # Run LLM analysis for more nuanced detection
        llm_result = self.detect_crisis_llm(message) if self.enable_llm else None
        
        # Combine results
        if llm_result is None:
            return keyword_result
        
        # Take the higher crisis level (more cautious approach)
        crisis_levels_order = [
            CrisisLevel.NO_CRISIS,
            CrisisLevel.LOW_RISK, 
            CrisisLevel.MODERATE_RISK,
            CrisisLevel.HIGH_RISK,
            CrisisLevel.IMMEDIATE_DANGER
        ]
        
        keyword_level_idx = crisis_levels_order.index(keyword_result.crisis_level)
        llm_level_idx = crisis_levels_order.index(llm_result.crisis_level)
        
        if llm_level_idx > keyword_level_idx:
            # LLM detected higher risk
            return CrisisDetectionResult(
                crisis_level=llm_result.crisis_level,
                confidence=min(llm_result.confidence, 0.9),  # Cap confidence for LLM
                reasoning=f"LLM analysis: {llm_result.reasoning}",
                triggered_by="both" if keyword_level_idx > 0 else "llm",
                immediate_action_needed=llm_result.immediate_action_needed,
                recommended_response=llm_result.recommended_response
            )
        elif keyword_level_idx > llm_level_idx:
            # Keywords detected higher risk
            return CrisisDetectionResult(
                crisis_level=keyword_result.crisis_level,
                confidence=keyword_result.confidence,
                reasoning=f"Keywords: {keyword_result.reasoning}; LLM: {llm_result.reasoning}",
                triggered_by="both",
                immediate_action_needed=keyword_result.immediate_action_needed,
                recommended_response=keyword_result.recommended_response
            )
        else:
            # Same level - combine confidence
            avg_confidence = (keyword_result.confidence + llm_result.confidence) / 2
            return CrisisDetectionResult(
                crisis_level=keyword_result.crisis_level,
                confidence=min(avg_confidence * 1.1, 1.0),  # Slight boost for agreement
                reasoning=f"Both methods agree: {llm_result.reasoning}",
                triggered_by="both",
                immediate_action_needed=keyword_result.immediate_action_needed or llm_result.immediate_action_needed,
                recommended_response=keyword_result.recommended_response
            )
    
    def _map_crisis_level_to_response(self, crisis_level: CrisisLevel) -> str:
        # Map crisis level to recommended response type
        mapping = {
            CrisisLevel.IMMEDIATE_DANGER: "emergency_crisis",
            CrisisLevel.HIGH_RISK: "urgent_crisis", 
            CrisisLevel.MODERATE_RISK: "supportive_crisis",
            CrisisLevel.LOW_RISK: "general_support",
            CrisisLevel.NO_CRISIS: "normal"
        }
        return mapping.get(crisis_level, "normal")

def test_crisis_detection():
    # Test the crisis detection system with various scenarios

    print("Testing LLM-Enhanced Crisis Detection System")
    print("=" * 60)
    
    # Initialize detector
    detector = LLMCrisisDetector(enable_llm=True)
    
    test_cases = [
        # Immediate danger cases
        ("I want to kill myself", CrisisLevel.IMMEDIATE_DANGER),
        ("He has a gun and is threatening me right now", CrisisLevel.IMMEDIATE_DANGER),
        ("I can't do this anymore, I want to die", CrisisLevel.IMMEDIATE_DANGER),
        
        # High risk cases
        ("He choked me last night and said he'll kill me", CrisisLevel.HIGH_RISK),
        ("Things are escalating badly, I'm really scared", CrisisLevel.HIGH_RISK),
        ("He won't let me leave the house anymore", CrisisLevel.HIGH_RISK),
        
        # Moderate risk cases
        ("I'm so scared and don't know what to do", CrisisLevel.MODERATE_RISK),
        ("I feel hopeless, everything is falling apart", CrisisLevel.MODERATE_RISK),
        ("I'm really worried about what might happen", CrisisLevel.MODERATE_RISK),
        
        # Low risk / general support
        ("I need information about my legal rights", CrisisLevel.LOW_RISK),
        ("Can you help me understand domestic violence?", CrisisLevel.NO_CRISIS),
        ("Hi, I'm looking for support services", CrisisLevel.NO_CRISIS),
    ]
    
    for message, expected_level in test_cases:
        print(f"\nTest: '{message}'")
        result = detector.detect_crisis_hybrid(message)
        
        print(f"Detected: {result.crisis_level.value} (confidence: {result.confidence:.2f})")
        print(f"Expected: {expected_level.value}")
        print(f"Reasoning: {result.reasoning}")
        print(f"Triggered by: {result.triggered_by}")
        print("-" * 50)

if __name__ == "__main__":
    test_crisis_detection()