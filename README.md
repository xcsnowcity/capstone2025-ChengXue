# RAG-based Chatbot for Domestic Abuse Support in Ireland

## Project Overview

This repository contains a MSc Computer Science (Data Analytics) capstone project: a specialized conversational AI chatbot designed to provide safe, accurate, and localized support for domestic violence survivors in Ireland using Retrieval-Augmented Generation (RAG) technology.

## Key Features

- **Hybrid Conversational AI**: Combines empathetic conversation with intelligent resource delivery
- **Irish-specific Knowledge Base**: Comprehensive content from Irish domestic violence organizations
- **Crisis Detection**: Real-time crisis detection with emergency escalation protocols

## System Architecture

### Core Components

1. **HybridDomesticViolenceChatbot** (`hybrid_chatbot.py`)
   - Main orchestration system combining conversation and resource delivery
   - Context-aware conversation management
   - Automatic RAG triggering based on user needs

2. **DomesticViolenceRAG** (`rag_pipeline.py`)
   - Advanced RAG implementation with multi-LLM support
   - Semantic search over Irish domestic violence content
   - Source attribution and citation

3. **LLMCrisisDetector** (`llm_crisis_detector.py`)
   - Multi-level crisis assessment (immediate danger, high risk, moderate, low)
   - Context-aware detection distinguishing crisis from information-seeking
   - Emergency protocol integration

4. **Knowledge Base Processing** (`main.py`)
   - Document processing and vector storage
   - ChromaDB integration with persistent storage
   - Metadata tagging and content organization

5. **Web Application** (`app_hybrid.py`, `app.py`)
   - Flask-based web interface with safety features
   - Responsive design with quick exit functionality
   - Fallback systems for robust operation

## Knowledge Base

The system includes a comprehensive knowledge base of Irish domestic violence resources:

- **Safe Ireland**: 100+ articles covering legal rights, support services, and safety planning
- **Women's Aid**: Comprehensive support information and contact details
- **HSE**: Health service resources and trauma-informed care guidelines
- **Citizens Information**: Government services and legal procedures
- **Crawl4AI Content**: Systematically extracted content from official Irish DV websites

### Content Sources
- Legal: Domestic Violence Act 2018, Courts Service, Legal Aid Board
- NGOs: Safe Ireland, Women's Aid, COPE Galway, Men's Aid
- Government: Department of Justice, Tusla, Citizens Information, HSE

## Installation and Setup

### Prerequisites
- Python 3.8+
- 4GB+ RAM
- 2GB storage space

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd capstone2025-ChengXue
   ```

2. **Install dependencies using uv**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

4. **Initialize the knowledge base**
   ```bash
   uv run python main.py
   ```

5. **Run the web application**
   ```bash
   uv run python app_hybrid.py
   ```

### Environment Configuration

Required environment variables:
```
OPENAI_API_KEY=your_openai_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
FLASK_SECRET_KEY=your_secret_key_here
```

## Usage

### Web Interface

1. Navigate to `http://localhost:5001`
2. Use the chat interface to interact with the chatbot
3. Quick exit button available for safety
4. Privacy and safety information accessible from main interface

### API Usage

The system provides RESTful API endpoints:

- `POST /chat` - Send message to chatbot
- `GET /health` - System health check
- `GET /privacy` - Privacy policy information
- `GET /safety` - Safety resources and emergency contacts

## Validation

### Technical Validation
- **RAGAS Metrics**: Faithfulness, relevance, context precision/recall
- **Performance Testing**: Response time, accuracy, system reliability
- **Safety Testing**: Crisis detection accuracy, emergency protocol validation

## Safety and Ethics

### Safety Features
- **Crisis Detection**: Immediate identification of users in danger
- **Emergency Escalation**: Automatic routing to emergency services (999/112)
- **Quick Exit**: Persistent exit button clearing session data
- **Anonymous Sessions**: No PII storage or tracking

### Privacy Compliance
- **No Data Persistence**: Conversations not stored permanently
- **Anonymous Access**: No user registration or identification required
- **Transparent Policies**: Clear privacy and data handling information
- **Session Management**: Automatic cleanup and history clearing

## Technical Specifications

### System Requirements
- **Runtime**: Python 3.8+ with uv dependency management
- **Database**: ChromaDB with persistent vector storage
- **LLM Providers**: OpenAI GPT models, OpenRouter, or local Ollama
- **Memory**: Minimum 4GB RAM for optimal performance
- **Storage**: 2GB for knowledge base and vector database

## File Structure

```
├── hybrid_chatbot.py              # Main chatbot orchestration
├── rag_pipeline.py               # RAG implementation
├── llm_crisis_detector.py        # Crisis detection system
├── main.py                       # Knowledge base processing
├── app_hybrid.py                 # Production web application
├── rag_validation.py             # Validation framework
├── crawl4ai_sitemap_crawler.py   # Content extraction
├── trauma_informed_delivery.py   # Ethical content delivery
├── Knowledge Base/               # Irish DV content
│   ├── safeireland_markdown/     # Safe Ireland resources
│   ├── womensaid/               # Women's Aid content
│   ├── hse/                     # Health service materials
│   └── crawl4ai_content/        # Extracted web content
├── templates/                    # Web interface templates
├── static/                       # CSS, JavaScript, assets
├── chroma_db/                    # Vector database 
```

## Deployment

### Local Deployment
```bash
uv run python app_hybrid.py
```

## Acknowledgments

This project was developed with support and guidance from:
- Domain experts in Irish domestic violence organizations TUSLA (https://www.tusla.ie/)
- Academic supervisor