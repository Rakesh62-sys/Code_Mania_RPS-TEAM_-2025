import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    # Create students table
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 student_id TEXT UNIQUE,
                 name TEXT,
                 encoding BLOB,
                 date_added TEXT)''')
    
    # Create attendance table
    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 student_id TEXT,
                 date TEXT,
                 time TEXT,
                 FOREIGN KEY(student_id) REFERENCES students(student_id))''')
    
    conn.commit()
    conn.close()

def add_student(student_id, name, encoding):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    # Convert numpy array to bytes for storage
    encoding_bytes = encoding.tobytes()
    
    c.execute("INSERT INTO students (student_id, name, encoding, date_added) VALUES (?, ?, ?, ?)",
              (student_id, name, encoding_bytes, datetime.now().strftime("%Y-%m-%d")))
    
    conn.commit()
    conn.close()

def mark_attendance(student_id):
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")
    
    # Check if already marked today
    c.execute("SELECT * FROM attendance WHERE student_id=? AND date=?", (student_id, current_date))
    if not c.fetchone():
        c.execute("INSERT INTO attendance (student_id, date, time) VALUES (?, ?, ?)",
                  (student_id, current_date, current_time))
    
    conn.commit()
    conn.close()

def get_student_encodings():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    c.execute("SELECT student_id, name, encoding FROM students")
    students = []
    
    for row in c.fetchall():
        student_id, name, encoding_bytes = row
        # Convert bytes back to numpy array
        encoding = np.frombuffer(encoding_bytes, dtype=np.float64)
        students.append((student_id, name, encoding))
    
    conn.close()
    return students