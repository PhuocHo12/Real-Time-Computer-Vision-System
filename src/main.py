import asyncio
import uvicorn
from fastapi import FastAPI

from config.loader import load_config, load_class_names
from camera.manager import CameraManager
from camera.registry import CameraRegistry
from vision.detector import YoloDetector
from pipeline.processor import VisionProcessor
from postprocess.tracking import TrackingPostProcessor
from tracking.bytetrack import ByteTrackTracker
from pipeline.broadcasters.ws import WebSocketBroadcaster
from api.ws import manager
from api.ws import router as ws_router
from pipeline.draw import Drawer
from pipeline.processors.draw import DrawProcessor
from fastapi.staticfiles import StaticFiles
# -------------------
# Load config
# -------------------
config = load_config()
class_names = load_class_names(config.detector.classes)

# -------------------
# FastAPI app
# -------------------
app = FastAPI()
app.include_router(ws_router)

# serve frontend
app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)
# -------------------
# Core components
# -------------------
registry = CameraRegistry()
detector = YoloDetector(config.detector)

drawer = Drawer(
    class_names=class_names,
    show_score=True,
    show_track_id=True,
)

post_processors = []

if config.tracking.enabled:
    tracker = ByteTrackTracker()
    post_processors.append(TrackingPostProcessor(tracker))

# Always draw
post_processors.append(DrawProcessor(drawer))


# -------------------
# Startup hook
# -------------------
@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()

    ws_broadcaster = WebSocketBroadcaster(manager, loop)

    processor = VisionProcessor(
        detector=detector,
        post_processors=post_processors,
        broadcaster=ws_broadcaster,
    )

    camera_manager = CameraManager(processor, registry)

    for cam in config.cameras:
        print(f"Registering camera {cam.camera_id} → {cam.source}")
        camera_manager.add_camera(
            cam.camera_id,
            cam.source,
            cam.fps_limit,
        )
@app.get("/index")
def read_index():
    return {"message": "Welcome to the Real-Time Computer Vision System"}

# -------------------htop

# Entry
# -------------------
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)