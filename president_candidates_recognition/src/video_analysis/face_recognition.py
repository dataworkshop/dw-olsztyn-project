import numpy as np
import cv2
import face_recognition
from src.helpers.color_log import setup_logger


class FaceRecognizer:

    def __init__(self, recognition_model="face_recognition"):
        if recognition_model == "face_recognition":
            self.recognizer = FaceRecognition()
        else:
            raise ValueError("Unknown recognition model")

    def recognize(self, frame, face_locations, known_names, known_encodings, draw_names=True):
        # build face encodings
        face_encodings = self.recognizer.encode(frame, face_locations)

        # compare encodings with known faces
        names = [
            self.compare_faces(encoding, known_encodings, known_names)
            for encoding in face_encodings
        ]

        if draw_names:
            # annotate face boxes with names
            for location, name in zip(face_locations, names):
                (top, right, bottom, left) = location
                y = top - 15 if top - 15 > 15 else top + 15
                cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2,)

        return frame, names

    def compare_faces(self, encoding, known_encodings, known_names, tolerance=0.45):
        """
        Compare distances between encodings and return name of closest one
        if distance is lower than tolerance
        """
        compare_distance = self.recognizer.distance(known_encodings, encoding)
        closest_index = np.argsort(compare_distance)[0]
        closest_distance = compare_distance[closest_index]
        name = known_names[closest_index] if closest_distance < tolerance else "UNKNOWN"

        return name


class FaceRecognition:

    def __init__(self):
        self._logger = setup_logger("FaceRecognition")
        self.encode = face_recognition.face_encodings
        self.distance = face_recognition.face_distance
