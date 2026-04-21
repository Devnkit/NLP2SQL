import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Database ka structure AI ko batao
DB_SCHEMA = """
Tables in the database:
1. students (id, name, grade, created_at)
2. courses (id, name, category)
3. enrollments (id, student_id, course_id, enrolled_at)

Relationships:
- enrollments.student_id → students.id
- enrollments.course_id → courses.id
"""

def convert_to_sql(question: str) -> str:
    """
    English question → SQL query
    OpenAI ko bolte hain: yeh question hai, yeh schema hai, SQL banao
    """
    
    prompt = f"""
You are an expert SQL generator for an EdTech database.

Database Schema:
{DB_SCHEMA}

User Question: {question}

Rules:
- Generate ONLY a SELECT query
- No DELETE, UPDATE, DROP, INSERT allowed
- Return ONLY the SQL query, nothing else
- Use proper JOINs when needed
- Use strftime('%Y', enrolled_at) for year filtering in SQLite
"""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a SQL expert. Return only SQL queries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0  # consistent results ke liye
    )
    
    sql = response.choices[0].message.content.strip()
    
    # SQL backticks remove karo (AI kabhi kabhi ```sql likhta hai)
    sql = sql.replace("```sql", "").replace("```", "").strip()
    
    # ✅ Safety Check — sirf SELECT allowed
    validate_sql(sql)
    
    return sql

def validate_sql(sql: str):
    """Dangerous queries block karo"""
    sql_upper = sql.upper().strip()
    
    blocked = ["DELETE", "DROP", "UPDATE", "INSERT", "ALTER", "CREATE", "TRUNCATE"]
    
    for keyword in blocked:
        if keyword in sql_upper:
            raise ValueError(f"❌ '{keyword}' queries are not allowed! Only SELECT is permitted.")
    
    if not sql_upper.startswith("SELECT"):
        raise ValueError("❌ Only SELECT queries are allowed.")