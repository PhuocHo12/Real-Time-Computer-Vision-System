import cv2
from .base import FrameProvider

class VideoProvider(FrameProvider):
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)

    def read(self):
        ret, frame = self.cap.read()
        return frame if ret else None

    def release(self):
        self.cap.release()