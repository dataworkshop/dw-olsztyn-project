from datetime import datetime
import cv2

from src.data.video.video_sources import info_channels
from src.data.faces.face_encodings import FaceEncodings
from src.video_analysis.face_detection import FaceDetector
from src.video_analysis.face_recognition import FaceRecognizer
from src.video_analysis.video_grabber.video_grabber import VideoGrabber
from src.db_manager.db_manager import DBManager
from src.db_manager.db_config import db_config
from src.helpers.image_montage import montage_frames
from src.helpers.color_log import setup_logger


def candidates_recognition():
    # turn on display functions and other details
    debug = True
    logger = setup_logger("Candidates")

    # load known faces data
    faces_path = "src/data/faces/president_candidates_faces/president_faces_df.pickle"
    known_names, known_encodings = FaceEncodings(faces_path).load_lists()

    # load face detector
    fd = FaceDetector(detection_model="caffe_ssd")

    # load face recognizer
    fr = FaceRecognizer(recognition_model="face_recognition")

    # video streams setup
    vg = VideoGrabber(video_sources=info_channels, scaling_factor=4)

    # database manager setup
    db = DBManager(db_config)
    db.setup_table()

    # recognitions grabber
    last_recognitions = {}

    # main loop
    while True:
        if vg.is_ready():

            # grab frames
            frames = vg.get_current_frames()

            # loop over the frames
            for source, frame in frames.items():

                # detect faces on frame
                frame, face_locations = fd.detector.detect(frame, min_confidence=0.7, draw_boxes=debug)

                if len(face_locations) > 0:
                    # recognize faces in found locations
                    frame, names = fr.recognize(frame, face_locations, known_names, known_encodings, draw_names=debug)

                    for name in names:
                        if name != "UNKNOWN":
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            if debug:
                                logger.info(f"Recognized: {name} @ {source}")

                            # verify last seen timestamp
                            if last_recognitions.get(f"{source} {name}") != timestamp:
                                db.insert_data(timestamp, name, source)
                                last_recognitions[f"{source} {name}"] = timestamp

            if debug:
                # show the output frames as montage
                montage = montage_frames(list(frames.values()))
                cv2.imshow("Captured_frames", montage)
                key = cv2.waitKey(1) & 0xFF

                # press q to quit
                if key == ord("q"):
                    break

                # press s to save montage
                if key == ord("s"):
                    cv2.imwrite(f"saved_montages/{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.jpg", montage)

    # cleanup
    cv2.destroyAllWindows()

if __name__ == '__main__':
    candidates_recognition()