#!/usr/bin/env python3
# Simple RAG Pipeline Demo without external LLM dependencies
# Uses template-based responses for demonstration purposes.

import re
from typing import List, Dict, Any, Optional
from main import KnowledgeBaseProcessor

class SimpleRAG:
    # Simple RAG implementation with template-based responses.
    
    def __init__(self):
        self.kb_processor = KnowledgeBaseProcessor()
        
        # Crisis keywords
        self.crisis_keywords = [
            "suicide", "kill myself", "want to die", "end it all", "can't go on",
            "going to hurt", "emergency", "in danger", "threatening me",
            "has a weapon", "going to kill", "immediate danger", "hurt myself",
            "harm myself", "suicidal", "end my life"
        ]
        
        # Response templates for common queries
        self.response_templates = {
            "coercive_control": """**Coercive Control in Ireland**

Based on Irish domestic violence resources:

{context}

**Key Points:**
- Coercive control became a criminal offence in Ireland in 2019
- It carries penalties of up to 5 years imprisonment
- It's defined as persistent controlling, coercive or threatening behavior

**Get Help:**
- Women's Aid 24/7 Helpline: **1800 341 900**
- Text "Hi" to **50818** for instant message support
- Free legal advice: Legal Aid Board

*You deserve support and you're not alone.*""",
            
            "safety_order": """**Getting a Safety Order in Ireland**

{context}

**Important Information:**
- Safety orders prevent someone from threatening or using violence
- Applications can be made to your local District Court
- You don't need a solicitor, but legal advice is recommended

**Next Steps:**
- Contact Women's Aid: **1800 341 900** for guidance
- Free legal advice: Legal Aid Board
- Court accompaniment services available

*Taking steps to protect yourself shows incredible strength.*""",
            
            "support_services": """**Support Services Available**

{context}

**National Resources:**
- Women's Aid 24/7 Helpline: **1800 341 900**
- Safe Ireland: safeireland.ie
- Citizens Information: citizensinformation.ie

**Local Services:**
{local_services}

*Every survivor deserves compassionate, professional support.*""",
            
            "general": """**Information from Irish Domestic Violence Organizations**

{context}

**Additional Support:**
- Women's Aid 24/7 Helpline: **1800 341 900** (free, confidential)
- Text "Hi" to **50818** for instant message support
- Safe Ireland: safeireland.ie

*Remember: You are not alone, and help is available.*"""
        }
    
    def detect_crisis(self, query: str) -> bool:
        # Detect crisis indicators.
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in self.crisis_keywords)
    
    def get_crisis_response(self) -> str:
        # Return immediate crisis response.
        return """**IMMEDIATE HELP NEEDED**

**If you're in immediate danger:**
- Call **999** or **112** for emergency services
- Women's Aid 24/7 Helpline: **1800 341 900** (free, confidential)

**For immediate emotional support:**
- Samaritans: **116 123** (free, 24/7)
- Text "HELLO" to **50808** (crisis text line)

**You don't have to face this alone. Trained professionals are available right now to help you.**

*If someone might see this conversation, use the quick exit feature for your safety.*"""
    
    def classify_query(self, query: str) -> str:
        # Classify query type for appropriate template.
        query_lower = query.lower()
        
        if any(term in query_lower for term in ["coercive control", "controlling", "coercion"]):
            return "coercive_control"
        elif any(term in query_lower for term in ["safety order", "protection order", "court order"]):
            return "safety_order"
        elif any(term in query_lower for term in ["support", "services", "help", "dublin", "cork", "galway"]):
            return "support_services"
        else:
            return "general"
    
    def extract_location(self, query: str) -> Optional[str]:
        # Extract location from query.
        counties = [
            "dublin", "cork", "galway", "limerick", "waterford", "kilkenny",
            "wexford", "carlow", "laois", "kildare", "meath", "wicklow",
            "louth", "monaghan", "cavan", "longford", "westmeath", "offaly",
            "tipperary", "clare", "kerry", "mayo", "sligo", "leitrim",
            "roscommon", "donegal"
        ]
        
        query_lower = query.lower()
        for county in counties:
            if county in query_lower:
                return county.title()
        return None
    
    def format_context(self, retrieved_docs: List[Dict[str, Any]], max_length: int = 300) -> str:
        # Format retrieved context for display.
        if not retrieved_docs:
            return "No specific information found in knowledge base."
        
        formatted_parts = []
        for doc in retrieved_docs[:3]:  # Use top 3 results
            content = doc['content'][:max_length]
            if len(doc['content']) > max_length:
                content += "..."
            
            org = doc['metadata']['organization']
            formatted_parts.append(f"**[{org}]** {content}")
        
        return "\n\n".join(formatted_parts)
    
    def get_local_services(self, location: Optional[str], retrieved_docs: List[Dict[str, Any]]) -> str:
        """Extract local services information."""
        if not location:
            return "Contact Women's Aid to find services in your area."
        
        # Look for location-specific information in retrieved docs
        local_info = []
        for doc in retrieved_docs:
            if location.lower() in doc['metadata'].get('county', '').lower():
                content = doc['content'][:150]
                if len(doc['content']) > 150:
                    content += "..."
                local_info.append(f"- {content}")
        
        if local_info:
            return f"**Services in {location}:**\n" + "\n".join(local_info[:2])
        else:
            return f"Contact Women's Aid at 1800 341 900 for specific services in {location}."
    
    def process_query(self, query: str) -> Dict[str, Any]:
        # Process query and return structured response.

        # Crisis detection
        if self.detect_crisis(query):
            return {
                "response": self.get_crisis_response(),
                "is_crisis": True,
                "sources": [],
                "metadata": {"crisis_detected": True}
            }
        
        # Retrieve context
        retrieved_docs = self.kb_processor.search_knowledge_base(query, n_results=5)
        
        if not retrieved_docs:
            return {
                "response": """I don't have specific information about that, but you can get comprehensive help from:

**Women's Aid 24/7 Helpline: 1800 341 900** (free, confidential)
**Safe Ireland:** safeireland.ie  
**Citizens Information:** citizensinformation.ie

These organizations have trained staff who can provide detailed guidance.""",
                "is_crisis": False,
                "sources": [],
                "metadata": {"no_context_found": True}
            }
        
        # Classify query and get appropriate template
        query_type = self.classify_query(query)
        template = self.response_templates[query_type]
        
        # Format context
        context = self.format_context(retrieved_docs)
        
        # Handle location-specific queries
        location = self.extract_location(query)
        local_services = ""
        if query_type == "support_services":
            local_services = self.get_local_services(location, retrieved_docs)
        
        # Generate response using template
        response = template.format(
            context=context,
            local_services=local_services
        )
        
        # Prepare sources
        sources = []
        for doc in retrieved_docs[:3]:
            metadata = doc['metadata']
            sources.append({
                "organization": metadata['organization'],
                "content_type": metadata['content_type'],
                "relevance": 1 - doc['distance'],
                "location": metadata.get('county', 'National')
            })
        
        return {
            "response": response,
            "is_crisis": False,
            "sources": sources,
            "metadata": {
                "query_type": query_type,
                "location": location,
                "num_sources": len(retrieved_docs)
            }
        }

def demo_simple_rag():
    # Demonstrate the simple RAG pipeline.

    print("🇮Simple RAG Pipeline Demo")
    print("=" * 60)
    print("Using template-based responses with retrieved context")
    print()
    
    rag = SimpleRAG()
    
    test_queries = [
        "What is coercive control?",
        "How do I get a safety order?", 
        "I need support services in Dublin",
        "I want to hurt myself",  # Crisis test
        "What happens when I call the Gardaí?",
        "Help with housing after leaving abuse"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\nQuery {i}: '{query}'")
        print("-" * 50)
        
        result = rag.process_query(query)
        
        if result['is_crisis']:
            print("**CRISIS RESPONSE TRIGGERED**")
        
        print(result['response'])
        
        if result['sources']:
            print(f"\n**Sources ({len(result['sources'])}):**")
            for j, source in enumerate(result['sources'], 1):
                rel_pct = source['relevance'] * 100
                print(f"  {j}. [{source['organization']}] {source['content_type']} "
                      f"({source['location']}) - Relevance: {rel_pct:.1f}%")
    
    print(f"\n" + "=" * 60)
    print("Simple RAG Demo Complete")
    print("Ready for production LLM integration or Open WebUI")

if __name__ == "__main__":
    demo_simple_rag()