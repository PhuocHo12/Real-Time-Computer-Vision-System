from dataclasses import dataclass
from typing import Any, List, Optional
import time

@dataclass
class FrameContext:
    camera_id: str
    frame: Any
    timestamp: float
    objects: List