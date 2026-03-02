import cv2
from .base import FrameProvider

class ImageProvider(FrameProvider):
    def __init__(self, path):
        self.frame = cv2.imread(path)
        self.used = False

    def read(self):
        if self.used:
            return None
        self.used = True
        return self.frame

    def release(self):
        pass