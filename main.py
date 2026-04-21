from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
from app.database import create_tables, get_connection
from app.nlp2sql import convert_to_sql
from app.stats import log_query, get_stats

app = FastAPI(title="NLP2SQL EdTech API")

# App start hone pe tables banao
@app.on_event("startup")
def startup():
    create_tables()

# Input ka format define karo
class QueryRequest(BaseModel):
    question: str

# ✅ POST /query — Main endpoint
@app.post("/query")
def query_endpoint(request: QueryRequest):
    question = request.question
    
    start_time = time.time()
    
    # Step 1: English → SQL
    sql = convert_to_sql(question)
    
    # Step 2: SQL ko database pe chalao
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        
        # Result format karo
        result = [dict(row) for row in rows]
        if len(result) == 1 and len(result[0]) == 1:
            result = list(result[0].values())[0]  # sirf number hai toh direct do
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SQL Error: {str(e)}")
    
    execution_time = round(time.time() - start_time, 4)
    
    # Analytics ke liye log karo
    log_query(question, sql, execution_time)
    
    return {
        "question": question,
        "generated_sql": sql,
        "result": result,
        "execution_time_seconds": execution_time
    }

# ✅ GET /stats — Analytics endpoint
@app.get("/stats")
def stats_endpoint():
    return get_stats()