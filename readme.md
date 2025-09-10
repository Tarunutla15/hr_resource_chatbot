# 🔎 HR Resource Query Chatbot

## 📖 Overview

An intelligent AI-powered HR assistant that helps teams find employees using natural language queries. Built with a RAG (Retrieval-Augmented Generation) architecture, this chatbot understands queries like "Find Python developers with healthcare experience" and returns relevant candidates with detailed explanations.

## ✨ Features

- **Natural Language Processing**: Understands complex HR queries in plain English
- **Hybrid Search System**: Combines keyword filtering with semantic search using embeddings
- **Dual Response Generation**: LLM-powered responses (Ollama) with template fallback
- **Real-time API**: FastAPI backend with instant response times
- **Beautiful UI**: Streamlit frontend with candidate cards and visual indicators
- **Smart Query Expansion**: Automatically understands synonyms and related terms
- **Availability Tracking**: Filters based on current employee availability status

## 🏗️ Architecture

```
User Query → Streamlit Frontend → FastAPI Backend → RAG Service → Hybrid Retrieval → Response Generation → User
```

### Components

- **Frontend**: Streamlit web application
- **Backend**: FastAPI REST API
- **Embedding Model**: sentence-transformers/all-mpnet-base-v2
- **LLM**: Ollama (Mistral) with fallback templates
- **Data Storage**: JSON-based employee database

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip package manager
- Hugging Face account and access token
- (Optional) Ollama for LLM responses

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd hr-resource-chatbot
```

2. **Set up Python virtual environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. **Set up Hugging Face token**

   **Create a token:**
   - Go to [Hugging Face Settings → Access Tokens](https://huggingface.co/settings/tokens)
   - Click "New token" → give it a name → choose "Read" role → copy it

   **Login in your environment:**
   ```bash
   pip install huggingface_hub
   huggingface-cli login
   ```
   Paste your token when prompted. This saves the token in your local cache.

4. **Set up backend**
```bash
cd backend
pip install -r requirements.txt
```

5. **Set up frontend**
```bash
cd ../frontend
pip install streamlit requests
```

6. **Run the application**
```bash
# Terminal 1 - Start backend
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Start frontend  
cd frontend
streamlit run streamlit_app.py
```

7. **Access the application**
   - Frontend: http://localhost:8501
   - API Docs: http://localhost:8000/docs

## 📊 API Documentation

### POST /chat/
Process natural language HR queries and return matching candidates.

**Request:**
```json
{
  "query": "Find Python developers with healthcare experience",
  "top_k": 5
}
```

**Response:**
```json
{
  "answer": "Based on your requirements, I found 3 excellent candidates...",
  "candidates": [
    {
      "employee": {
        "id": 1,
        "name": "Alice Johnson",
        "skills": ["Python", "React", "AWS"],
        "experience_years": 5,
        "projects": ["E-commerce Platform", "Healthcare Dashboard"],
        "availability": "available",
        "role": "Full Stack Engineer",
        "notes": "Worked on healthcare dashboard integrating backend ML microservices."
      },
      "score": 0.892
    }
  ]
}
```

### GET /employees/search?query=python&skills=react
Programmatic employee search endpoint.

## 🔧 Configuration

Environment variables (optional via .env.example file):

```bash
EMBEDDING_MODEL=sentence-transformers/all-mpnet-base-v2
TOP_K=5
USE_OLLAMA=false
OLLAMA_MODEL=mistral
EMPLOYEE_DATA_PATH=data/employees.json
```

### Interesting AI-Generated Solutions
- **Hybrid Search Algorithm**: AI suggested combining keyword filtering with semantic search for better accuracy
- **Query Expansion**: Automated synonym mapping (e.g., "automation" → "CI/CD", "DevOps")
- **Graceful Fallbacks**: AI helped design the Ollama → template fallback system
- **Embedding Optimization**: Suggested precomputed embeddings with ID mapping

### Manual Solutions
- **Performance Optimization**: Hand-coded embedding reuse system
- **Error Handling**: Custom exception handling for production readiness
- **UI/UX Design**: Manual Streamlit layout and styling
- **Data Modeling**: Custom Pydantic models for type safety

## ⚙️ Technical Decisions

### Why Hybrid Search?
Chose hybrid approach because:
- Keyword filtering ensures mandatory skill requirements are met
- Semantic search captures contextual meaning and related concepts
- Combined approach provides better accuracy than either method alone

### Why Local LLM (Ollama) vs Cloud API?
- **Privacy**: Employee data never leaves local infrastructure
- **Cost**: No ongoing API costs for production use
- **Latency**: Faster response times without network calls
- **Offline Capability**: Works without internet connection

### Performance vs Cost vs Privacy Trade-offs

| Aspect | Choice | Rationale |
|--------|--------|-----------|
| Embeddings | Local sentence-transformers | Free, fast, no data leaving premises |
| LLM | Ollama (optional) | Privacy-first, cost-effective |
| Vector Search | In-memory | Simple, no additional infrastructure |
| Storage | JSON files | Easy development, suitable for small datasets |

## 📈 Performance

- **Average Response Time**: < 2 seconds
- **Embedding Load Time**: ~3 seconds (cold start)
- **Query Processing**: < 1 second
- **Memory Usage**: ~500MB (including embedding model)

## 🧪 Testing

Test with these example queries:

```bash
1. "Find Python developers with 3+ years experience"
2. "Who has worked on healthcare projects?"
3. "Suggest people for a React Native project"
4. "Find developers who know both AWS and Docker"
5. "Available ML engineers with cloud experience"
```

## 🔮 Future Improvements

With more time, I would add:

- **Persistence Layer**: PostgreSQL with pgvector for larger datasets
- **Authentication**: JWT-based auth for enterprise use
- **Advanced Filtering**: Experience range, location, salary filters
- **Chat History**: Persistent conversation memory
- **Multi-modal Search**: Support for PDF resumes and documents
- **Admin Panel**: CRUD interface for employee management
- **Deployment**: Docker containers and Kubernetes orchestration
- **Monitoring**: Performance metrics and usage analytics
- **Caching**: Redis for frequent query results
- **Webhooks**: Integration with HR systems like Greenhouse/Lever

## 🎯 Demo

### Screenshots
- Chat Interface: `screenshots/chat-interface.png`
- Candidate Results: `screenshots/candidate-results.png`

## 📝 License

MIT License - feel free to use this project for learning and development purposes.

## 🤝 Contributing

1. **Fork the repository**
```bash
git clone https://github.com/yourusername/hr-resource-chatbot.git
```

2. **Create a feature branch**
```bash
git checkout -b feature/amazing-feature
```

3. **Commit changes**
```bash
git commit -m 'Add amazing feature'
```

4. **Push to branch**
```bash
git push origin feature/amazing-feature
```

5. **Open a Pull Request**

## 📞 Support

For questions or issues:
- Check the API Documentation
- Review the example queries
- Open an issue on GitHub

---

Built with ❤️ using modern AI-assisted development practices

## 🔧 Troubleshooting

### Common Issues

1. **Hugging Face Token Error**
   ```bash
   # Make sure you're logged in
   huggingface-cli login
   # Verify token is saved
   huggingface-cli whoami
   ```

2. **Virtual Environment Issues**
   ```bash
   # Make sure venv is activated (you should see (venv) in terminal)
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Port Already in Use**
   ```bash
   # Change port if 8000 is busy
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
   ```

4. **Memory Issues**
   ```bash
   # If embedding model doesn't load, try:
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   ```