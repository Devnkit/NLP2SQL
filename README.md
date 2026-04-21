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


