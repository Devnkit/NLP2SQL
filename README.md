pip install -r requirements.txt
uvicorn app.main:app --reload
docker build -t nlp2sql-app .
docker run -p 8000:8000 nlp2sql-app
pytest