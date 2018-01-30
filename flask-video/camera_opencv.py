import cv2
from base_camera import BaseCamera

class Camera(BaseCamera):
    def __init__(self, idx):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.idx = idx
        self.video = cv2.VideoCapture(idx)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        try:
            success, image = self.video.read()
            res = cv2.resize(image, (320, 320))
            ret, jpeg = cv2.imencode('.jpg', res)
            return jpeg.tobytes()
        except:
            self.video.release()
            self.video = cv2.VideoCapture(self.idx)
            success, image = self.video.read()
            res = cv2.resize(image, (320, 320))
            ret, jpeg = cv2.imencode('.jpg', res)
            return jpeg.tobytes()
