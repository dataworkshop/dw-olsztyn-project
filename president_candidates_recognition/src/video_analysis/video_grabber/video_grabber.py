import threading
import copy
import cv2
from src.helpers.color_log import setup_logger


class VideoGrabber:

    def __init__(self, video_sources, scaling_factor=1):
        self._logger = setup_logger("VideoGrabber")
        self.video_sources = video_sources
        self.scaling_factor = scaling_factor
        self.frames = {}
        self.run()

    def get_current_frames(self):
        return copy.deepcopy(self.frames)

    def run(self):

        for name, url in self.video_sources.items():
            thread = threading.Thread(
                target=self.run_source_thread, args=(name, url), daemon=True
            )
            thread.start()

            self._logger.info(f"Thread: {name} started")

    def run_source_thread(self, name, url):

        cap = cv2.VideoCapture(url)

        while True:

            ret, frame = cap.read()
            if frame is None:
                continue

            if self.scaling_factor > 1:

                height, width, _ = frame.shape

                new_height = height / self.scaling_factor
                new_width = width / self.scaling_factor

                frame = cv2.resize(frame, (int(new_width), int(new_height)))

            self.frames[name] = frame

    def is_ready(self):
        return len(self.frames) == len(self.video_sources)
