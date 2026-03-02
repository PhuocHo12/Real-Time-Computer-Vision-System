# camera config & state
from enum import Enum
from dataclasses import dataclass, field
from typing import Optional, Dict
import time

class CameraStatus(str, Enum):
    STOPPED = "stopped"
    RUNNING = "running"
    ERROR = "error"

@dataclass
class CameraConfig:
    camera_id: str
    source: str
    fps_limit: int = 10

@dataclass
class CameraState:
    status: CameraStatus = CameraStatus.STOPPED
    last_frame_ts: Optional[float] = None
    fps: float = 0.0
    error: Optional[str] = None

    _frame_count: int = field(default=0, repr=False)
    _start_ts: float = field(default_factory=time.time, repr=False)

    def update_frame(self):
        self._frame_count += 1
        self.last_frame_ts = time.time()

        elapsed = self.last_frame_ts - self._start_ts
        if elapsed > 0:
            self.fps = self._frame_count / elapsed

class CameraRegistry:
    def __init__(self):
        self._configs: Dict[str, CameraConfig] = {}
        self._states: Dict[str, CameraState] = {}

    def register(self, config: CameraConfig):
        if config.camera_id in self._configs:
            raise ValueError(f"Camera {config.camera_id} already exists")

        self._configs[config.camera_id] = config
        self._states[config.camera_id] = CameraState()

    def unregister(self, camera_id: str):
        self._configs.pop(camera_id, None)
        self._states.pop(camera_id, None)

    def set_status(self, camera_id: str, status: CameraStatus, error: str = None):
        state = self._states.get(camera_id)
        if not state:
            return

        state.status = status
        state.error = error

    def update_frame(self, camera_id: str):
        state = self._states.get(camera_id)
        if state:
            state.update_frame()

    def get_state(self, camera_id: str) -> Optional[CameraState]:
        return self._states.get(camera_id)

    def list_cameras(self):
        return [
            {
                "camera_id": cid,
                "source": self._configs[cid].source,
                "fps_limit": self._configs[cid].fps_limit,
                "status": self._states[cid].status,
                "fps": round(self._states[cid].fps, 2),
                "last_frame_ts": self._states[cid].last_frame_ts,
                "error": self._states[cid].error,
            }
            for cid in self._configs
        ]