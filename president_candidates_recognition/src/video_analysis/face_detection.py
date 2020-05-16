import cv2
import numpy as np
from src.data.models.models import CaffeSSD
from src.helpers.color_log import setup_logger


class FaceDetector:

    def __init__(self, detection_model="caffe_ssd"):
        if detection_model == "caffe_ssd":
            self.detector = CaffeSSDDetector()
        else:
            raise ValueError("Unknown detection model")


class CaffeSSDDetector:

    def __init__(self):
        self._net = CaffeSSD.load()
        self._logger = setup_logger("CaffeSSDDetector")

    def detect(self, frame, min_confidence=0.7, draw_boxes=True):

        # face locations list
        face_locations = []

        # grab the frame dimensions and convert it to a blob
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0)
        )

        # pass the blob through the network and obtain the detections and
        # predictions
        self._net.setInput(blob)
        detections = self._net.forward()

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            if confidence < min_confidence:
                continue

            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the bounding box of the face
            if draw_boxes:
                cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 0, 255), 2)

            # keep face location in face_recognition format
            face_locations.append((startY, endX, endY, startX))

        if face_locations:
            self._logger.debug(f"Found {len(face_locations)} faces: {face_locations}")

        return frame, face_locations
