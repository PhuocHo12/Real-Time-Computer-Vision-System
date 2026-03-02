import time
import logging
from .context import FrameContext

class VisionProcessor:
    def __init__(self, detector, post_processors=None, broadcaster=None):
        self.detector = detector
        self.post_processors = post_processors or []
        self.broadcaster = broadcaster
        self.logger = logging.getLogger(self.__class__.__name__)

    def process(self, frame, camera_id):
        ctx = FrameContext(
            camera_id=camera_id,
            frame=frame,
            timestamp=time.time(),
            objects=[]
        )

        # 1. Detect (frame → objects)
        ctx.objects = self.detector.infer(ctx.frame)

        # 2. Post-process (tracking, draw, analytics)
        for p in self.post_processors:
            ctx = p.process(ctx)

        # 3. Broadcast (frame + metadata)
        if self.broadcaster:
            self.broadcaster.send(ctx)

        return ctx