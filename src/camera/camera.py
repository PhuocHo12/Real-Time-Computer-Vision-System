# execution single camera pipeline
import threading
import time
import cv2
import logging
from .registry import CameraStatus
class CameraPipeline:
    def __init__(
        self,
        camera_id,
        source,
        processor,
        registry,
        fps_limit=10,
    ):
        self.camera_id = camera_id
        self.source = source
        self.processor = processor  # VisionProcessor (FrameContext-based)
        self.registry = registry
        self.fps_limit = fps_limit
        self._cap = None
        self._thread = None
        self._running = False

        self.logger = logging.getLogger(
            f"CameraPipeline[{camera_id}]"
        )

    # -------------------------
    # Lifecycle
    # -------------------------

    def start(self):
        if self._running:
            self.logger.warning("Camera already running")
            return

        self._cap = cv2.VideoCapture(self.source)
        if not self._cap.isOpened():
            self.registry.set_status(
                self.camera_id,
                CameraStatus.ERROR,
                "Failed to open video source",
            )
            self.logger.error("Failed to open video source")
            return

        self._running = True
        self._thread = threading.Thread(
            target=self._run,
            name=f"CameraThread-{self.camera_id}",
            daemon=True,  # allow clean shutdown
        )
        self._thread.start()

    def stop(self):
        if not self._running:
            return

        self._running = False

        if self._thread:
            self._thread.join(timeout=2.0)

        if self._cap:
            self._cap.release()
            self._cap = None

        self.registry.set_status(
            self.camera_id,
            CameraStatus.STOPPED,
        )

    # -------------------------
    # Internal loop
    # -------------------------

    def _run(self):
        frame_interval = 1.0 / max(self.fps_limit, 1)

        self.registry.set_status(
            self.camera_id,
            CameraStatus.RUNNING,
        )

        self.logger.info("Camera loop started")

        while self._running:
            loop_start = time.time()

            ret, frame = self._cap.read()
            if not ret:
                self.registry.set_status(
                    self.camera_id,
                    CameraStatus.ERROR,
                    "Frame capture failed",
                )
                self.logger.error("Frame capture failed")
                break

            # Update heartbeat / frame count
            self.registry.update_frame(self.camera_id)

            try:
                # Vision pipeline (FrameContext flows inside)
                self.processor.process(frame, self.camera_id)
                # Optionally put the processed frame into a queue for streaming
            except Exception as e:
                self.logger.exception("Vision processing failed")
                self.registry.set_status(
                    self.camera_id,
                    CameraStatus.ERROR,
                    "Processing failed",
                )
                break

            # FPS limiting
            elapsed = time.time() - loop_start
            sleep_time = frame_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

        if self._cap:
            self._cap.release()
            self._cap = None

        self.logger.info("Camera loop exited")