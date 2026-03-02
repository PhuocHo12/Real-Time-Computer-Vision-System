import cv2
import json
import base64
import asyncio


class WebSocketBroadcaster:
    def __init__(self, manager, loop: asyncio.AbstractEventLoop):
        self.manager = manager
        self.loop = loop

    def send(self, ctx):
        ok, jpeg = cv2.imencode(".jpg", ctx.frame)
        if not ok:
            return

        payload = {
            "camera_id": ctx.camera_id,
            "timestamp": ctx.timestamp,
            "image": base64.b64encode(jpeg).decode("utf-8"),
            "objects": ctx.objects,
        }

        message = json.dumps(payload)

        # SAFE cross-thread call
        self.loop.call_soon_threadsafe(
            asyncio.create_task,
            self.manager.broadcast(message),
        )