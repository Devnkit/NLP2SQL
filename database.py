import sqlite3
from datetime import datetime

DB_PATH = "edtech.db"
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT
        )
    """)
    
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (course_id) REFERENCES courses(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Tables created!")

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    
    students = [
        ("Rahul Sharma", "10th"), ("Priya Singh", "12th"),
        ("Amit Kumar", "11th"), ("Neha Gupta", "10th"),
        ("Rohan Verma", "12th"), ("Anjali Mehta", "11th"),
        ("Deepak Joshi", "10th"), ("Pooja Patel", "12th"),
        ("Vikram Rao", "11th"), ("Sunita Das", "10th")
    ]
    cursor.executemany(
        "INSERT INTO students (name, grade) VALUES (?, ?)", students
    )
    
    
    courses = [
        ("Python Programming", "Technology"),
        ("Machine Learning", "AI"),
        ("Web Development", "Technology"),
        ("Data Science", "AI"),
        ("Mathematics", "Science")
    ]
    cursor.executemany(
        "INSERT INTO courses (name, category) VALUES (?, ?)", courses
    )
    
  
    enrollments = [
        (1, 1, "2024-01-15"), (1, 2, "2024-02-10"),
        (2, 1, "2024-01-20"), (2, 3, "2024-03-05"),
        (3, 2, "2024-02-14"), (3, 4, "2024-04-01"),
        (4, 1, "2024-01-25"), (4, 5, "2024-05-10"),
        (5, 3, "2024-03-12"), (5, 2, "2024-02-28"),
        (6, 1, "2024-01-30"), (6, 4, "2024-04-15"),
        (7, 2, "2024-02-18"), (7, 3, "2024-03-22"),
        (8, 1, "2024-01-10"), (8, 5, "2024-06-01"),
        (9, 4, "2024-04-20"), (9, 1, "2024-01-05"),
        (10, 2, "2024-02-22"), (10, 3, "2024-03-30"),
    ]
    cursor.executemany(
        "INSERT INTO enrollments (student_id, course_id, enrolled_at) VALUES (?, ?, ?)",
        enrollments
    )
    
    conn.commit()
    conn.close()
    print("✅ Sample data added!")


if __name__ == "__main__":
    create_tables()
    seed_data()