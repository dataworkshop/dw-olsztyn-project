import cv2


class CaffeSSD:
    _prototxt = "src/data/models/ssd_face_detector_model/deploy.prototxt"
    _model = "src/data/models/ssd_face_detector_model/res10_300x300_ssd_iter_140000.caffemodel"

    @classmethod
    def load(cls):
        return cv2.dnn.readNetFromCaffe(cls._prototxt, cls._model)
