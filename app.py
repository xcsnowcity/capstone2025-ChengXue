#!/usr/bin/env python3

import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS

# Import our RAG pipeline and conversation flow
try:
    from rag_pipeline import DomesticViolenceRAG
    from conversation_flow import ConversationManager, UserProfile, ConversationStage
    from intelligent_conversation_manager import IntelligentConversationManager
    RAG_CLASS = DomesticViolenceRAG
    RAG_TYPE = "full"
    CONVERSATION_FLOW = True
    INTELLIGENT_CONVERSATION = True
except ImportError as e:
    print(f"Warning: Could not import full RAG pipeline: {e}")
    print("Falling back to simple RAG...")
    from rag_simple import SimpleRAG
    RAG_CLASS = SimpleRAG
    RAG_TYPE = "simple"
    CONVERSATION_FLOW = False
    INTELLIGENT_CONVERSATION = False

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)

# Initialize RAG pipeline and conversation manager
print(f"Initializing {RAG_TYPE} RAG pipeline...")
if RAG_TYPE == "full":
    # Initialize with OpenRouter/OpenAI
    llm_provider = os.getenv('LLM_PROVIDER', 'openrouter')
    default_model = 'anthropic/claude-3.5-haiku' if llm_provider == 'openrouter' else 'gpt-4o-mini'
    
    rag_pipeline = RAG_CLASS(
        llm_provider=llm_provider,
        model_name=os.getenv('LLM_MODEL', default_model),
        max_context_chunks=int(os.getenv('MAX_CONTEXT_CHUNKS', '5')),
        temperature=float(os.getenv('TEMPERATURE', '0.3'))
    )
    print(f"✅ Full {llm_provider.upper()} RAG pipeline initialized with {rag_pipeline.model_name}")
    
    # Initialize intelligent conversation manager
    if INTELLIGENT_CONVERSATION:
        try:
            intelligent_conversation_manager = IntelligentConversationManager(
                llm_provider=llm_provider,
                model_name=default_model,
                temperature=0.3
            )
            print(f"✅ Intelligent Conversation Manager initialized")
        except Exception as e:
            print(f"⚠️ Could not initialize Intelligent Conversation Manager: {e}")
            INTELLIGENT_CONVERSATION = False
            intelligent_conversation_manager = None
    else:
        intelligent_conversation_manager = None
else:
    # Fallback to simple template-based
    rag_pipeline = RAG_CLASS()
    intelligent_conversation_manager = None
    print("⚠️ Using template-based RAG (OpenAI not available)")

# Session configuration for safety
app.config.update(
    SESSION_COOKIE_SECURE=False,  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=1800  # 30 minutes
)

# Helper functions for session management
def get_user_profile_from_session():
    profile_data = session.get('user_profile', {})
    
    # Handle safety level enum
    from conversation_flow import SafetyLevel
    safety_level_str = profile_data.get('safety_level', 'unknown')
    if isinstance(safety_level_str, str):
        try:
            safety_level = SafetyLevel(safety_level_str)
        except ValueError:
            safety_level = SafetyLevel.UNKNOWN
    else:
        safety_level = safety_level_str
    
    return UserProfile(
        session_id=session.get('session_id', 'unknown'),
        safety_level=safety_level,
        location=profile_data.get('location'),
        county=profile_data.get('county'),
        relationship_status=profile_data.get('relationship_status'),
        has_children=profile_data.get('has_children'),
        children_ages=profile_data.get('children_ages', []),
        employment_status=profile_data.get('employment_status'),
        housing_situation=profile_data.get('housing_situation'),
        support_network=profile_data.get('support_network'),
        immigration_status=profile_data.get('immigration_status'),
        disability_status=profile_data.get('disability_status'),
        primary_concern=profile_data.get('primary_concern'),
        help_seeking_history=profile_data.get('help_seeking_history'),
        readiness_level=profile_data.get('readiness_level'),
        preferred_contact=profile_data.get('preferred_contact')
    )

def update_session_profile(user_profile: UserProfile):
    profile_dict = user_profile.__dict__.copy()
    # Convert enum to string for JSON serialization
    profile_dict['safety_level'] = user_profile.safety_level.value
    session['user_profile'] = profile_dict

def handle_fallback_conversation(user_message: str):
    try:
        if CONVERSATION_FLOW:
            user_profile = get_user_profile_from_session()
            current_stage = ConversationStage(session.get('conversation_stage', ConversationStage.GREETING.value))
            
            result = rag_pipeline.process_conversational_query(
                user_message, user_profile, current_stage
            )
            
            update_session_profile(result['profile_update'])
            session['conversation_stage'] = result['conversation_stage'].value
            
            return {
                'message': result['response'],
                'is_crisis': result.get('is_crisis', False),
                'sources': result.get('sources', []),
                'timestamp': datetime.now().isoformat(),
                'session_id': session['session_id'],
                'rag_type': RAG_TYPE,
                'model_used': getattr(rag_pipeline, 'model_name', 'template') if RAG_TYPE == "full" else 'template',
                'conversation_mode': 'fallback',
                'conversation_stage': result['conversation_stage'].value
            }
        else:
            # Ultimate fallback
            result = rag_pipeline.process_query(user_message)
            return {
                'message': result['response'],
                'is_crisis': result.get('is_crisis', False),
                'sources': result.get('sources', []),
                'timestamp': datetime.now().isoformat(),
                'session_id': session['session_id'],
                'rag_type': RAG_TYPE,
                'model_used': getattr(rag_pipeline, 'model_name', 'template') if RAG_TYPE == "full" else 'template',
                'conversation_mode': 'fallback'
            }
    except Exception as e:
        app.logger.error(f"Fallback conversation error: {str(e)}")
        return {
            'message': """I'm here to support you, though I'm having technical difficulties right now. 

For immediate help, please contact:
- **Women's Aid 24/7 Helpline: 1800 341 900** (free, confidential)
- **Emergency: 999 or 112**

Your safety is the priority.""",
            'is_crisis': False,
            'sources': [],
            'timestamp': datetime.now().isoformat(),
            'session_id': session.get('session_id', 'unknown'),
            'rag_type': RAG_TYPE,
            'conversation_mode': 'error'
        }

@app.route('/')
def index():
    # Always start fresh for safety - clear any existing session
    session.clear()
    
    # Generate unique session ID for anonymity
    session['session_id'] = str(uuid.uuid4())
    session['chat_history'] = []
    
    # Initialize conversation flow
    if CONVERSATION_FLOW:
        profile = UserProfile(session_id=session['session_id'])
        profile_dict = profile.__dict__.copy()
        # Convert enum to string for JSON serialization
        profile_dict['safety_level'] = profile.safety_level.value
        session['user_profile'] = profile_dict
        session['conversation_stage'] = ConversationStage.GREETING.value
        session['is_first_message'] = True
    
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        user_response_length = data.get('response_length', 'adaptive')
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Handle intelligent conversation flow if available
        if INTELLIGENT_CONVERSATION and intelligent_conversation_manager:
            # Get user profile from session and reconstruct UserProfile object
            user_profile = get_user_profile_from_session()
            
            # Get conversation history for context
            conversation_history = session.get('chat_history', [])
            
            # Use intelligent conversation manager to decide next action
            try:
                decision = intelligent_conversation_manager.process_message(
                    user_message, user_profile, conversation_history
                )
                
                # Handle different actions
                if decision['action'] == 'crisis_mode':
                    # Crisis detected - immediate response
                    response = {
                        'message': decision['response'],
                        'is_crisis': True,
                        'sources': [],
                        'timestamp': datetime.now().isoformat(),
                        'session_id': session['session_id'],
                        'rag_type': RAG_TYPE,
                        'model_used': getattr(rag_pipeline, 'model_name', 'template') if RAG_TYPE == "full" else 'template',
                        'conversation_mode': 'crisis',
                        'confidence': decision.get('confidence', 1.0),
                        'reasoning': decision.get('reasoning', 'Crisis detected')
                    }
                    
                elif decision['action'] == 'use_rag':
                    # User needs specific information - use RAG pipeline
                    if CONVERSATION_FLOW:
                        # Use conversational RAG with current context
                        # Prioritize user's frontend choice, then decision, then default
                        response_length = user_response_length if user_response_length != 'adaptive' else decision.get('response_length', 'adaptive')
                        result = rag_pipeline.process_conversational_query(
                            user_message, user_profile, ConversationStage.ONGOING_SUPPORT, 
                            include_sources=True, response_length=response_length
                        )
                        
                        response = {
                            'message': result['response'],
                            'is_crisis': result.get('is_crisis', False),
                            'sources': result.get('sources', []),
                            'timestamp': datetime.now().isoformat(),
                            'session_id': session['session_id'],
                            'rag_type': RAG_TYPE,
                            'model_used': getattr(rag_pipeline, 'model_name', 'template') if RAG_TYPE == "full" else 'template',
                            'conversation_mode': 'rag',
                            'confidence': decision.get('confidence', 0.8),
                            'reasoning': decision.get('reasoning', 'Specific information requested'),
                            'personalized': result['metadata'].get('personalized', False)
                        }
                    else:
                        # Fallback to simple RAG
                        result = rag_pipeline.process_query(user_message)
                        response = {
                            'message': result['response'],
                            'is_crisis': result.get('is_crisis', False),
                            'sources': result.get('sources', []),
                            'timestamp': datetime.now().isoformat(),
                            'session_id': session['session_id'],
                            'rag_type': RAG_TYPE,
                            'model_used': getattr(rag_pipeline, 'model_name', 'template') if RAG_TYPE == "full" else 'template',
                            'conversation_mode': 'rag'
                        }
                        
                else:  # continue_conversation
                    # Continue natural conversation
                    response = {
                        'message': decision['response'],
                        'is_crisis': False,
                        'sources': [],
                        'timestamp': datetime.now().isoformat(),
                        'session_id': session['session_id'],
                        'rag_type': RAG_TYPE,
                        'model_used': getattr(rag_pipeline, 'model_name', 'template') if RAG_TYPE == "full" else 'template',
                        'conversation_mode': 'conversation',
                        'confidence': decision.get('confidence', 0.7),
                        'reasoning': decision.get('reasoning', 'Continuing supportive conversation'),
                        'profile_updates': decision.get('profile_updates', {})
                    }
                
                # Update user profile with any new information
                if decision.get('profile_updates'):
                    user_profile = intelligent_conversation_manager.update_user_profile(
                        user_profile, decision['profile_updates']
                    )
                    update_session_profile(user_profile)
                    
            except Exception as e:
                app.logger.error(f"Intelligent conversation manager error: {str(e)}")
                # Fallback to original conversation flow
                response = handle_fallback_conversation(user_message)
                
        # Fallback to original conversation flow if intelligent conversation not available        
        elif CONVERSATION_FLOW:
            # Original conversation flow logic (keeping as fallback)
            user_profile = get_user_profile_from_session()
            current_stage = ConversationStage(session.get('conversation_stage', ConversationStage.GREETING.value))
            
            result = rag_pipeline.process_conversational_query(
                user_message, user_profile, current_stage
            )
            
            # Update session with profile changes
            profile_dict = result['profile_update'].__dict__.copy()
            profile_dict['safety_level'] = result['profile_update'].safety_level.value
            session['user_profile'] = profile_dict
            session['conversation_stage'] = result['conversation_stage'].value
            
            response = {
                'message': result['response'],
                'is_crisis': result.get('is_crisis', False),
                'sources': result.get('sources', []),
                'timestamp': datetime.now().isoformat(),
                'session_id': session['session_id'],
                'rag_type': RAG_TYPE,
                'model_used': getattr(rag_pipeline, 'model_name', 'template') if RAG_TYPE == "full" else 'template',
                'conversation_stage': result['conversation_stage'].value,
                'profile_completeness': result['metadata'].get('profile_completeness', 0),
                'is_guided': result['metadata'].get('prompt_type') in ['safety_assessment', 'location_assessment', 'relationship_assessment', 'children_assessment', 'needs_assessment'],
                'personalized': result['metadata'].get('personalized', False)
            }
        else:
            # Fallback to original RAG pipeline
            result = rag_pipeline.process_query(user_message)
            
            # Prepare response
            response = {
                'message': result['response'],
                'is_crisis': result.get('is_crisis', False),
                'sources': result.get('sources', []),
                'timestamp': datetime.now().isoformat(),
                'session_id': session['session_id'],
                'rag_type': RAG_TYPE,
                'model_used': getattr(rag_pipeline, 'model_name', 'template') if RAG_TYPE == "full" else 'template'
            }
        
        # Store in session history (for current session only, not persistent)
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        # Limit history to last 10 exchanges for memory management
        session['chat_history'].append({
            'user': user_message,
            'bot': response['message'],
            'timestamp': response['timestamp'],
            'is_crisis': response.get('is_crisis', False)
        })
        
        # Keep only last 10 exchanges
        if len(session['chat_history']) > 10:
            session['chat_history'] = session['chat_history'][-10:]
        
        return jsonify(response)
        
    except Exception as e:
        app.logger.error(f"Chat error: {str(e)}")
        return jsonify({
            'message': """I'm experiencing technical difficulties. For immediate support, please contact:

**Women's Aid 24/7 Helpline: 1800 341 900** (free, confidential)
**Emergency: 999 or 112**

Your safety is the priority.""",
            'error': True,
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/quick-exit', methods=['POST'])
def quick_exit():
    """Handle quick exit - clear session and redirect."""
    try:
        # Clear all session data
        session.clear()
        
        return jsonify({
            'status': 'success',
            'redirect_url': 'https://www.google.ie',
            'message': 'Session cleared. Redirecting to Google...'
        })
        
    except Exception as e:
        app.logger.error(f"Quick exit error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Error clearing session'
        }), 500

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear chat history for current session."""
    try:
        session['chat_history'] = []
        return jsonify({'status': 'success', 'message': 'Chat history cleared'})
    except Exception as e:
        app.logger.error(f"Clear history error: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Error clearing history'}), 500

@app.route('/api/status')
def status():
    """API status check."""
    try:
        # Test RAG pipeline
        test_result = rag_pipeline.process_query("test")
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'rag_available': True,
            'rag_type': RAG_TYPE,
            'model_used': getattr(rag_pipeline, 'model_name', 'template') if RAG_TYPE == "full" else 'template',
            'session_id': session.get('session_id', 'none')
        })
    except Exception as e:
        app.logger.error(f"Status check error: {str(e)}")
        return jsonify({
            'status': 'degraded',
            'error': str(e),
            'rag_available': False
        }), 500

@app.route('/privacy')
def privacy():
    """Privacy information page."""
    return render_template('privacy.html')

@app.route('/safety')
def safety():
    """Safety information page."""
    return render_template('safety.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Development server settings
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )