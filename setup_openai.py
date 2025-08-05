#!/usr/bin/env python3
import os
import sys
from pathlib import Path

def check_openai_installation():
    try:
        import openai
        print(" OpenAI library is installed")
        return True
    except ImportError:
        print(" OpenAI library not found")
        return False

def check_env_file():
    env_file = Path('.env')
    
    if not env_file.exists():
        print(" .env file not found")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
        
    # Check for either OpenRouter or OpenAI API key
    has_openrouter = 'OPENROUTER_API_KEY=' in content and 'your-openrouter-api-key-here' not in content
    has_openai = 'OPENAI_API_KEY=' in content and 'your-openai-api-key-here' not in content
    
    if has_openrouter or has_openai:
        provider = "OpenRouter" if has_openrouter else "OpenAI"
        print(f" .env file exists with {provider} API key")
        return True
    else:
        print(" .env file missing valid API key")
        return False

def create_env_file():
    print("\n Setting up .env file...")
    
    # Choose provider
    print("\nAvailable LLM providers:")
    print("1. OpenRouter (recommended - access to multiple models)")
    print("2. OpenAI (direct API)")
    print("3. Ollama (local models)")
    
    while True:
        choice = input("\nChoose provider [1]: ").strip() or "1"
        if choice in ['1', '2', '3']:
            break
        print(" Invalid choice. Please enter 1, 2, or 3.")
    
    if choice == '1':
        # OpenRouter setup
        api_key = input("Enter your OpenRouter API key: ").strip()
        if not api_key:
            print(" API key required")
            return False
        
        print("\nRecommended models:")
        print("1. anthropic/claude-3.5-haiku (fast, cost-effective)")
        print("2. anthropic/claude-3.5-sonnet (higher quality)")
        print("3. openai/gpt-4o-mini (good balance)")
        print("4. openai/gpt-4o (highest quality, more expensive)")
        
        model_choice = input("Choose model [1]: ").strip() or "1"
        models = {
            '1': 'anthropic/claude-3.5-haiku',
            '2': 'anthropic/claude-3.5-sonnet', 
            '3': 'openai/gpt-4o-mini',
            '4': 'openai/gpt-4o'
        }
        model = models.get(model_choice, 'anthropic/claude-3.5-haiku')
        
        env_content = f"""# Environment variables for Irish DV Support Chatbot

# LLM Provider Configuration
LLM_PROVIDER=openrouter

# OpenRouter API Configuration
OPENROUTER_API_KEY={api_key}

# Flask Configuration  
FLASK_SECRET_KEY={os.urandom(24).hex()}

# Model Configuration
LLM_MODEL={model}

# RAG Configuration
MAX_CONTEXT_CHUNKS=5
TEMPERATURE=0.3
"""
    
    elif choice == '2':
        # OpenAI setup
        api_key = input("Enter your OpenAI API key: ").strip()
        if not api_key or not api_key.startswith('sk-'):
            print(" Invalid OpenAI API key format. Should start with 'sk-'")
            return False
        
        model = input("Enter OpenAI model [gpt-4o-mini]: ").strip() or "gpt-4o-mini"
        
        env_content = f"""# Environment variables for Irish DV Support Chatbot

# LLM Provider Configuration
LLM_PROVIDER=openai

# OpenAI API Configuration
OPENAI_API_KEY={api_key}

# Flask Configuration  
FLASK_SECRET_KEY={os.urandom(24).hex()}

# Model Configuration
LLM_MODEL={model}

# RAG Configuration
MAX_CONTEXT_CHUNKS=5
TEMPERATURE=0.3
"""
    
    else:
        # Ollama setup
        model = input("Enter Ollama model [llama3.2]: ").strip() or "llama3.2"
        
        env_content = f"""# Environment variables for Irish DV Support Chatbot

# LLM Provider Configuration
LLM_PROVIDER=ollama

# Flask Configuration  
FLASK_SECRET_KEY={os.urandom(24).hex()}

# Model Configuration
LLM_MODEL={model}

# RAG Configuration
MAX_CONTEXT_CHUNKS=5
TEMPERATURE=0.3
"""

    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(" .env file created successfully")
    return True

def test_llm_connection():
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        provider = os.getenv('LLM_PROVIDER', 'openrouter')
        model = os.getenv('LLM_MODEL', 'anthropic/claude-3.5-haiku')
        
        if provider in ['openai', 'openrouter']:
            import openai
            
            if provider == 'openrouter':
                client = openai.OpenAI(
                    base_url="https://openrouter.ai/api/v1",
                    api_key=os.getenv('OPENROUTER_API_KEY'),
                )
            else:
                client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            # Test with a simple completion
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say hello"}
                ],
                max_tokens=10
            )
            
            print(f" {provider.upper()} API connection successful")
            print(f" Model: {model}")
            print(f" Test response: {response.choices[0].message.content}")
            return True
        
        elif provider == 'ollama':
            print(" Ollama configuration set up")
            print(f" Model: {model}")
            print(" Make sure Ollama is running: ollama serve")
            return True
        
    except Exception as e:
        print(f" {provider.upper()} API connection failed: {e}")
        return False

def main():
    print(" Irish DV Support Chatbot - LLM Setup")
    print("=" * 50)
    
    # Check dependencies
    openai_installed = check_openai_installation()
    env_configured = check_env_file()
    
    if not openai_installed:
        print("\n Installing OpenAI library...")
        os.system("uv add openai")
        openai_installed = check_openai_installation()
    
    if not env_configured:
        print("\n LLM Setup Required")
        print("Choose your preferred LLM provider:")
        print("- OpenRouter: Access to multiple models (Claude, GPT, etc.)")
        print("- OpenAI: Direct API access")
        print("- Ollama: Local models")
        
        setup = input("\nDo you want to set up your LLM provider now? (y/n): ").lower().strip()
        
        if setup == 'y':
            if create_env_file():
                env_configured = True
        else:
            print(" Skipping LLM setup. App will use template responses.")
            return
    
    # Test connection if everything is set up
    if openai_installed and env_configured:
        print("\n Testing LLM connection...")
        if test_llm_connection():
            print("\n Setup Complete!")
            print(" LLM integration ready")
            print(" Run: uv run python app.py")
        else:
            print("\n Setup incomplete - check your configuration")
    
    print("\n" + "=" * 50)
    print(" Tips:")
    print("- Keep your API key secure and never commit it to version control")
    print("- OpenRouter: Get API keys at https://openrouter.ai/")
    print("- Claude models are excellent for domestic violence support contexts")
    print("- Monitor your usage through your provider's dashboard")

if __name__ == "__main__":
    main()