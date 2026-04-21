# EdTech NLP-to-SQL API

A production-ready FastAPI backend service that converts natural language questions into SQL queries and returns answers from an EdTech database. Perfect for enabling non-technical users to query educational data.

## 🎯 Features

- **NLP-to-SQL Conversion**: Convert natural language questions to SQL queries using LLM-based approach
- **Safe Query Execution**: Only SELECT queries allowed, with comprehensive security checks
- **Analytics Tracking**: Track query metrics, keywords, and performance statistics
- **RESTful API**: Clean, well-documented API endpoints with automatic Swagger UI
- **Database Setup**: Pre-seeded EdTech database with students, courses, and enrollments
- **Comprehensive Testing**: Unit tests for database operations and API endpoints
- **Docker Support**: Containerized application with multi-stage builds
- **Kubernetes Ready**: Complete Kubernetes manifests with resource limits and auto-scaling
- **Production Grade**: Health checks, error handling, CORS support, and logging

## 📋 Prerequisites

- Python 3.11+
- OpenAI API Key (for LLM-based NLP-to-SQL conversion)
- pip or conda for package management
- Docker (optional, for containerization)
- Kubernetes (optional, for orchestration)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone 
cd edtech-nlp-sql-project

python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-xxxx...
```

### 3. Run the Application

```bash
python main.py
# OR
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit: `http://localhost:8000`

### 4. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### 1. Health Check
```
GET /health
```
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "version": "1.0.0"
}
```

### 2. Query Endpoint (Core Feature)
POST /query
**Request:**
```json
{ "question": "How many students enrolled in Python courses in 2024?" }
```
**Response:**
```json
{
  "original_question": "How many students enrolled in Python courses in 2024?",
  "generated_sql": "SELECT COUNT(DISTINCT e.student_id) as total_students FROM enrollments e JOIN courses c ON e.course_id = c.id WHERE c.name LIKE '%Python%' AND YEAR(e.enrolled_at) = 2024",
  "result": [{"total_students": 7}],
  "execution_time_ms": 12.5,
  "row_count": 1,
  "status": "success"
}
```

### 3. Analytics / Statistics
GET /stats
```json
{
  "total_queries": 15,
  "common_keywords": [
    {"keyword": "students", "count": 8},
    {"keyword": "courses", "count": 6}
  ],
  "slowest_queries": [{"question": "Complex query...", "execution_time_ms": 125.3}],
  "total_execution_time_ms": 450.2,
  "average_execution_time_ms": 30.01
}
```

### 4. Database Schema
GET /schema

### 5. Reset Analytics
POST /reset-stats

## 🗄️ Database Schema

### Students Table
```sql
CREATE TABLE students (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  grade INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Courses Table
```sql
CREATE TABLE courses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  category TEXT NOT NULL
);
```

### Enrollments Table
```sql
CREATE TABLE enrollments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  course_id INTEGER NOT NULL,
  enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (student_id) REFERENCES students(id),
  FOREIGN KEY (course_id) REFERENCES courses(id)
);
```

## 🤖 NLP-to-SQL Approach

Uses **LLM-based approach** (OpenAI GPT-3.5-turbo):

### Process Flow
1. **Parse Question** → Receive natural language question
2. **Add Context** → Inject database schema + sample data into prompt
3. **Generate SQL** → LLM generates SQL query
4. **Validate** → Ensure only SELECT queries are allowed
5. **Execute** → Run SQL safely with error handling
6. **Return Results** → Send results + metadata

### Security Measures
- Only SELECT queries allowed (DELETE, DROP, UPDATE, INSERT are blocked)
- Input validation and sanitization
- Dangerous keyword detection
- Exception handling with meaningful error messages

### Example Questions
- "How many students are enrolled in total?"
- "Which courses have the most enrollments?"
- "How many students enrolled in Python courses in 2024?"
- "Get the names of all students with grade 10 or higher"

## 🧪 Testing

```bash
pytest           # Run all tests
pytest -v        # Verbose output
pytest --cov=.   # With coverage
```

### Test Structure
- `tests/test_database.py` — Database operations & security
- `tests/test_api.py` — API endpoints & models
- `tests/test_nlp_to_sql.py` — NLP logic & keyword extraction

## 🐳 Docker

```bash
# Build
docker build -t edtech-nlp-sql-api:latest .

# Run
docker run -p 8000:8000 -e OPENAI_API_KEY=your-api-key edtech-nlp-sql-api:latest

# Docker Compose (easier)
docker-compose up -d
```

## ☸️ Kubernetes

```bash
kubectl create secret generic openai-credentials \
  --from-literal=api-key=your-api-key

kubectl apply -f kubernetes.yaml

kubectl get pods -l app=edtech-nlp-sql-api
kubectl logs edtech-nlp-sql-api
kubectl port-forward pod/edtech-nlp-sql-api 8000:8000
```

**Kubernetes Includes:**
- Pod with resource limits
- Service for load balancing
- ConfigMap + Secret management
- HorizontalPodAutoscaler (1–3 replicas)
- Liveness & readiness probes
- Non-root security context

## 📊 Performance

| Operation | Time |
|-----------|------|
| Simple SELECT | ~10–20ms |
| JOIN queries | ~15–30ms |
| Aggregations | ~20–50ms |
| LLM inference | ~500–2000ms |

## ⚠️ Limitations

1. Requires OpenAI API key and internet connectivity
2. LLM API calls incur costs
3. Very complex queries may not generate correctly
4. Performance depends on database size

## 🔒 Security Best Practices

- Use HTTPS in production
- Implement API authentication
- Use rate limiting
- Only SELECT queries allowed at DB level
- Non-root Docker containers
- Secrets managed via Kubernetes Secrets or `.env`

## 📝 Project Structure
edtech-nlp-sql-project/
├── main.py                 # FastAPI application
├── database.py             # Database operations
├── models.py               # Pydantic models
├── nlp_to_sql.py           # NLP to SQL conversion
├── utils.py                # Utility functions
├── tests/
│   ├── init.py
│   ├── test_api.py
│   ├── test_database.py
│   └── test_nlp_to_sql.py
├── Dockerfile
├── docker-compose.yml
├── kubernetes.yaml
├── requirements.txt
├── pytest.ini
├── .env.example
├── .gitignore
└── README.md

## 🆘 Troubleshooting

| Issue | Fix |
|-------|-----|
| API key not found | Add `OPENAI_API_KEY` to `.env` |
| Port 8000 in use | Use `--port 8001` |
| DB not created | Delete `edtech.db` and restart |
| Tests failing | Run `pip install -r requirements.txt` first |

## 🎓 Learning Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [LangChain Docs](https://python.langchain.com/)
- [OpenAI API Docs](https://platform.openai.com/docs/)
- [Kubernetes Docs](https://kubernetes.io/docs/)

---
