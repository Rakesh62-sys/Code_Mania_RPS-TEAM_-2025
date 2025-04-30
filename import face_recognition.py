import face_recognition
import cv2
import numpy as np
from database import get_student_encodings

class FaceRecognizer:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.known_face_ids = []
        self.load_known_faces()
        
    def load_known_faces(self):
        students = get_student_encodings()
        for student_id, name, encoding in students:
            self.known_face_encodings.append(encoding)
            self.known_face_names.append(name)
            self.known_face_ids.append(student_id)
    
    def recognize_faces(self, frame):
        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # Convert BGR to RGB
        rgb_small_frame = small_frame[:, :, ::-1]
        
        # Find all face locations and encodings
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        recognized_faces = []
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare with known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"
            student_id = None
            
            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
                student_id = self.known_face_ids[best_match_index]
                
                # Scale face locations back to original size
                top, right, bottom, left = face_location
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                recognized_faces.append({
                    'student_id': student_id,
                    'name': name,
                    'location': (top, right, bottom, left),
                    'confidence': 1 - face_distances[best_match_index]
                })
        
        return recognized_faces