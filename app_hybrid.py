#!/usr/bin/env python3
import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS

# Import our new hybrid chatbot
from hybrid_chatbot import HybridDomesticViolenceChatbot

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app)

# Initialize hybrid chatbot
try:
    llm_provider = os.getenv('LLM_PROVIDER', 'openrouter')
    default_model = 'anthropic/claude-3.5-haiku' if llm_provider == 'openrouter' else 'gpt-4o-mini'
    
    # Store chatbot instances per session (for conversation continuity)
    chatbot_instances = {}
    
    print(f"Hybrid chatbot configured with {llm_provider.upper()} / {default_model}")
except Exception as e:
    print(f"Error configuring hybrid chatbot: {e}")
    chatbot_instances = {}

# Session configuration for safety
app.config.update(
    SESSION_COOKIE_SECURE=False,  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=1800  # 30 minutes
)

def get_or_create_chatbot(session_id: str) -> HybridDomesticViolenceChatbot:
    
    if session_id not in chatbot_instances:
        try:
            llm_provider = os.getenv('LLM_PROVIDER', 'openrouter')
            default_model = 'anthropic/claude-3.5-haiku' if llm_provider == 'openrouter' else 'gpt-4o-mini'
            
            chatbot_instances[session_id] = HybridDomesticViolenceChatbot(
                llm_provider=llm_provider,
                model_name=os.getenv('LLM_MODEL', default_model),
                temperature=float(os.getenv('TEMPERATURE', '0.3'))
            )
        except Exception as e:
            app.logger.error(f"Failed to create chatbot for session {session_id}: {e}")
            raise
    
    return chatbot_instances[session_id]

def cleanup_old_sessions():
    if len(chatbot_instances) > 50:  # Arbitrary limit
        # Remove oldest instances (simple approach)
        oldest_keys = list(chatbot_instances.keys())[:10]
        for key in oldest_keys:
            del chatbot_instances[key]

@app.route('/')
def index():
    # Main page - start fresh session for safety
    # Always start fresh for safety - clear any existing session
    session.clear()
    
    # Generate unique session ID for anonymity
    session['session_id'] = str(uuid.uuid4())
    session['chat_history'] = []
    session['start_time'] = datetime.now().isoformat()
    
    # Clean up old sessions periodically
    cleanup_old_sessions()
    
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    # Main chat endpoint using hybrid chatbot
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        session_id = session.get('session_id')
        if not session_id:
            return jsonify({'error': 'No valid session'}), 400
        
        # Get or create chatbot instance for this session
        try:
            chatbot = get_or_create_chatbot(session_id)
        except Exception as e:
            app.logger.error(f"Failed to get chatbot instance: {e}")
            return jsonify({
                'message': """I'm experiencing technical difficulties. For immediate support, please contact:

**Women's Aid 24/7 Helpline: 1800 341 900** (free, confidential)
**Emergency: 999 or 112**

Your safety is the priority.""",
                'error': True,
                'timestamp': datetime.now().isoformat()
            }), 500
        
        # Process message with hybrid chatbot
        try:
            result = chatbot.generate_hybrid_response(user_message)
            
            # Prepare API response
            response = {
                'message': result['response'],
                'timestamp': datetime.now().isoformat(),
                'session_id': session_id,
                'conversation_mode': 'hybrid',
                'model_used': chatbot.model_name,
                
                # Hybrid-specific fields
                'type': result['type'],
                'rag_used': result['rag_used'],
                'resources_provided': result['resources_provided'],
                'context_triggers': result.get('context_triggers', []),
                
                # Crisis handling
                'is_crisis': result['type'] == 'crisis',
                'crisis_level': result.get('crisis_level'),
                
                # Conversation context for debugging (remove in production)
                'conversation_context': result.get('conversation_context', {}),
                'message_count': result.get('conversation_context', {}).get('message_count', 0)
            }
            
        except Exception as e:
            app.logger.error(f"Hybrid chatbot processing error: {str(e)}")
            # Fallback response
            response = {
                'message': """I'm having trouble responding right now, but I want you to know that help is available.

**Women's Aid 24/7 Helpline: 1800 341 900** (free, confidential)
**Emergency: 999 or 112**

Your safety matters.""",
                'error': True,
                'timestamp': datetime.now().isoformat(),
                'session_id': session_id,
                'conversation_mode': 'error'
            }
        
        # Store in session history (for current session only)
        if 'chat_history' not in session:
            session['chat_history'] = []
        
        session['chat_history'].append({
            'user': user_message,
            'bot': response['message'],
            'timestamp': response['timestamp'],
            'is_crisis': response.get('is_crisis', False),
            'rag_used': response.get('rag_used', False),
            'type': response.get('type', 'unknown')
        })
        
        # Keep only last 10 exchanges for memory management
        if len(session['chat_history']) > 10:
            session['chat_history'] = session['chat_history'][-10:]
        
        return jsonify(response)
        
    except Exception as e:
        app.logger.error(f"Chat endpoint error: {str(e)}")
        return jsonify({
            'message': """I'm experiencing technical difficulties. For immediate support, please contact:

**Women's Aid 24/7 Helpline: 1800 341 900** (free, confidential)
**Emergency: 999 or 112**

Your safety is the priority.""",
            'error': True,
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/api/conversation-summary', methods=['GET'])
def conversation_summary():
    """Get conversation summary for debugging/analysis"""
    try:
        session_id = session.get('session_id')
        if not session_id or session_id not in chatbot_instances:
            return jsonify({'error': 'No active conversation'}), 404
        
        chatbot = chatbot_instances[session_id]
        summary = chatbot.get_conversation_summary()
        
        return jsonify({
            'session_id': session_id,
            'summary': summary,
            'session_history': session.get('chat_history', []),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        app.logger.error(f"Conversation summary error: {str(e)}")
        return jsonify({'error': 'Could not get conversation summary'}), 500

@app.route('/api/quick-exit', methods=['POST'])
def quick_exit():
    """Handle quick exit - clear session and redirect"""
    try:
        session_id = session.get('session_id')
        
        # Remove chatbot instance if exists
        if session_id and session_id in chatbot_instances:
            del chatbot_instances[session_id]
        
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
    """Clear chat history for current session"""
    try:
        session_id = session.get('session_id')
        
        # Clear session history
        session['chat_history'] = []
        
        # Reset chatbot conversation state
        if session_id and session_id in chatbot_instances:
            chatbot = chatbot_instances[session_id]
            chatbot.conversation_history = []
            chatbot.conversation_context = chatbot.conversation_context.__class__()
        
        return jsonify({'status': 'success', 'message': 'Chat history cleared'})
    except Exception as e:
        app.logger.error(f"Clear history error: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Error clearing history'}), 500

@app.route('/api/status')
def status():
    """API status check"""
    try:
        session_id = session.get('session_id', 'test')
        
        # Test hybrid chatbot
        test_chatbot = get_or_create_chatbot(f"test_{datetime.now().timestamp()}")
        test_result = test_chatbot.generate_hybrid_response("test")
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'chatbot_available': True,
            'chatbot_type': 'hybrid',
            'model_used': test_chatbot.model_name,
            'session_id': session.get('session_id', 'none'),
            'active_sessions': len(chatbot_instances),
            'test_response_type': test_result.get('type', 'unknown')
        })
    except Exception as e:
        app.logger.error(f"Status check error: {str(e)}")
        return jsonify({
            'status': 'degraded',
            'error': str(e),
            'chatbot_available': False
        }), 500

@app.route('/privacy')
def privacy():
    """Privacy information page"""
    return render_template('privacy.html')

@app.route('/safety')
def safety():
    """Safety information page"""
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
        port=5001,  # Different port to avoid conflicts
        threaded=True
    )