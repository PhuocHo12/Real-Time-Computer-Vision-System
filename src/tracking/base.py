from abc import ABC, abstractmethod

class BaseTracker(ABC):

    @abstractmethod
    def update(self, detections):
        """
        detections: List of [x1, y1, x2, y2, score, class_id]
        returns: List of tracked objects
        """
        pass