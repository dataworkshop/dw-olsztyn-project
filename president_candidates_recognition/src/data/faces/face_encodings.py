import pandas as pd


class FaceEncodings:

    def __init__(self, data_path):
        self._data_path = data_path

    def load_lists(self):
        data = pd.read_pickle(self._data_path)

        known_names = data["name"].to_list()
        known_encodings = data["face_encodings"].to_list()

        return known_names, known_encodings
