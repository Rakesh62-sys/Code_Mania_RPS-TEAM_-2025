import cv
import os
import sqlite3
from datetime import datetime

# Simplified face detection (not recognition) using OpenCV
def simple_attendance_system():
    # Initialize database
    conn = sqlite3.connect('simple_attendance.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  date TEXT,
                  time TEXT)''')
    conn.commit()
    
    # Load OpenCV's face detector
    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Start webcam
    cap = cv.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Convert to grayscale
        gray = cv.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Mark attendance when face is detected
            current_time = datetime.now()
            c.execute("INSERT INTO attendance (date, time) VALUES (?, ?)",
                     (current_time.strftime("%Y-%m-%d"), current_time.strftime("%H:%M:%S")))
            conn.commit()
            print(f"Attendance marked at {current_time}")
        
        cv2.imshow('Simple Attendance System', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    conn.close()

if __name__ == "__main__":
    simple_attendance_system()