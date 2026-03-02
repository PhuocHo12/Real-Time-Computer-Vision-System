from abc import ABC, abstractmethod

class PostProcessor(ABC):

    @abstractmethod
    def process(self, detections, ctx):
        return detections
    
class TrackingPostProcessor(PostProcessor):
    def __init__(self, tracker):
        self.tracker = tracker

    def process(self, detections, frame_ctx):
        return self.tracker.update(detections)