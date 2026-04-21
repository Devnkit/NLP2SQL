import json
from datetime import datetime
from app.database import get_connection

# Pehle analytics table banao
def create_stats_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            sql_query TEXT,
            execution_time REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

create_stats_table()

def log_query(question: str, sql: str, execution_time: float):
    """Har query ko log karo"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO query_logs (question, sql_query, execution_time) VALUES (?, ?, ?)",
        (question, sql, execution_time)
    )
    conn.commit()
    conn.close()

def get_stats():
    """Analytics data nikalo"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Total queries
    cursor.execute("SELECT COUNT(*) as total FROM query_logs")
    total = cursor.fetchone()["total"]
    
    # Slowest query
    cursor.execute("""
        SELECT question, sql_query, execution_time 
        FROM query_logs 
        ORDER BY execution_time DESC 
        LIMIT 1
    """)
    slowest = cursor.fetchone()
    
    # Common keywords dhundho
    cursor.execute("SELECT question FROM query_logs")
    all_questions = [row["question"] for row in cursor.fetchall()]
    
    keywords = {}
    common_words = ["students", "courses", "enrolled", "python", "ml", "count", "how many", "list"]
    for q in all_questions:
        q_lower = q.lower()
        for word in common_words:
            if word in q_lower:
                keywords[word] = keywords.get(word, 0) + 1
    
    # Top 5 keywords
    top_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)[:5]
    
    conn.close()
    
    return {
        "total_queries": total,
        "top_keywords": [{"keyword": k, "count": v} for k, v in top_keywords],
        "slowest_query": dict(slowest) if slowest else None
    }