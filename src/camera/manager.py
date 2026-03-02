# lifecycle & registry
from .camera import CameraPipeline
import logging
class CameraManager:
    def __init__(self, processor, registry=None):
        self.processor = processor
        self.registry = registry
        self.cameras = {}
        self.logger = logging.getLogger(self.__class__.__name__)
    def add_camera(self, camera_id, source, fps_limit=10):
        if camera_id in self.cameras:
            raise ValueError(f"Camera {camera_id} already exists")

        pipeline = CameraPipeline(
            camera_id=camera_id,
            source=source,
            processor=self.processor,
            fps_limit=fps_limit,
            registry=self.registry,
        )
        pipeline.start()
        self.cameras[camera_id] = pipeline

    def remove_camera(self, camera_id):
        pipeline = self.cameras.pop(camera_id, None)
        if pipeline:
            pipeline.stop()

    def list_cameras(self):
        return list(self.cameras.keys())