import websocket

ws = websocket.WebSocket()
ws.connect("ws://192.168.60.103:8000/ws")

print("✅ Connected to WebSocket")

while True:
    msg = ws.recv()
    print("📩 Received:", msg)