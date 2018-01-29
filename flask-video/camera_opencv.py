import cv2
from base_camera import BaseCamera

class Camera(BaseCamera):
    def __init__(self, idx):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
		self.video = cv2.VideoCapture(idx)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if not success: 
            self.video = cv2.VideoCapture('xing.avi')
            success, image = self.video.read()
        res = cv2.resize(image, (320, 320))
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', res)
        return jpeg.tobytes()

class Camera1(BaseCamera):
    def __init__(self, idx):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        if idx == 1:
		    self.video = cv2.VideoCapture(idx)
        else:
            self.video = cv2.VideoCapture('tree.avi')

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if not success: 
            self.video = cv2.VideoCapture()
            success, image = self.video.read()
        res = cv2.resize(image, (320, 320))
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', res)
        return jpeg.tobytes()
