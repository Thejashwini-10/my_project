import sqlite3
from typing import List, Dict, Optional, Tuple

DB_PATH = "students.db"

def get_conn(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path: str = DB_PATH) -> None:
    conn = get_conn(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            roll TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS grades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_roll TEXT NOT NULL,
            subject TEXT NOT NULL,
            grade REAL NOT NULL CHECK(grade >= 0 AND grade <= 100),
            UNIQUE(student_roll, subject),
            FOREIGN KEY(student_roll) REFERENCES students(roll) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()

def add_student(name: str, roll: str, db_path: str = DB_PATH) -> bool:
    conn = get_conn(db_path)
    try:
        conn.execute("INSERT INTO students (roll, name) VALUES (?,?)", (roll.strip(), name.strip()))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def add_grade(roll: str, subject: str, grade: float, db_path: str = DB_PATH) -> Tuple[bool, str]:
    if not (0 <= grade <= 100):
        return False, "Grade must be between 0 and 100."
    conn = get_conn(db_path)
    try:
        # Ensure student exists
        s = conn.execute("SELECT 1 FROM students WHERE roll = ?", (roll,)).fetchone()
        if not s:
            return False, "Student not found."
        conn.execute("""
            INSERT INTO grades (student_roll, subject, grade) VALUES (?,?,?)
            ON CONFLICT(student_roll, subject) DO UPDATE SET grade=excluded.grade
        """, (roll, subject.strip().title(), float(grade)))
        conn.commit()
        return True, "Grade saved."
    finally:
        conn.close()

def get_student(roll: str, db_path: str = DB_PATH) -> Optional[Dict]:
    conn = get_conn(db_path)
    try:
        stu = conn.execute("SELECT roll, name FROM students WHERE roll = ?", (roll,)).fetchone()
        if not stu:
            return None
        grades = conn.execute("SELECT subject, grade FROM grades WHERE student_roll = ? ORDER BY subject", (roll,)).fetchall()
        grades_dict = {row["subject"]: row["grade"] for row in grades}
        avg = calculate_student_average(roll, db_path)
        return {"roll": stu["roll"], "name": stu["name"], "grades": grades_dict, "average": avg}
    finally:
        conn.close()

def list_students(db_path: str = DB_PATH) -> List[Dict]:
    conn = get_conn(db_path)
    try:
        rows = conn.execute("SELECT roll, name FROM students ORDER BY roll").fetchall()
        return [{"roll": r["roll"], "name": r["name"]} for r in rows]
    finally:
        conn.close()

def calculate_student_average(roll: str, db_path: str = DB_PATH) -> float:
    conn = get_conn(db_path)
    try:
        row = conn.execute("SELECT AVG(grade) as avg_grade FROM grades WHERE student_roll = ?", (roll,)).fetchone()
        return round(row["avg_grade"] if row and row["avg_grade"] is not None else 0.0, 2)
    finally:
        conn.close()

def subject_topper(subject: str, db_path: str = DB_PATH) -> Optional[Dict]:
    conn = get_conn(db_path)
    try:
        row = conn.execute("""
            SELECT s.name, s.roll, g.grade
            FROM grades g
            JOIN students s ON s.roll = g.student_roll
            WHERE g.subject = ?
            ORDER BY g.grade DESC, s.name ASC
            LIMIT 1
        """, (subject.strip().title(),)).fetchone()
        if row:
            return {"name": row["name"], "roll": row["roll"], "grade": row["grade"], "subject": subject.strip().title()}
        return None
    finally:
        conn.close()

def class_average(subject: str, db_path: str = DB_PATH) -> float:
    conn = get_conn(db_path)
    try:
        row = conn.execute("SELECT AVG(grade) AS avg_grade FROM grades WHERE subject = ?", (subject.strip().title(),)).fetchone()
        return round(row["avg_grade"] if row and row["avg_grade"] is not None else 0.0, 2)
    finally:
        conn.close()

def backup_to_csv(filepath: str, db_path: str = DB_PATH) -> None:
    import csv
    conn = get_conn(db_path)
    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["roll", "name", "subject", "grade"])
            for row in conn.execute("""
                SELECT s.roll, s.name, g.subject, g.grade
                FROM students s LEFT JOIN grades g ON s.roll = g.student_roll
                ORDER BY s.roll, g.subject
            """):
                writer.writerow([row["roll"], row["name"], row["subject"] if row["subject"] else "", row["grade"] if row["grade"] is not None else ""])
    finally:
        conn.close()
