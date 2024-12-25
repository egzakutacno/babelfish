from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from rtc import WebRTCServer

app = FastAPI()

# WebRTC signaling server
webrtc_server = WebRTCServer()

@app.get("/")
async def get_index():
    return FileResponse("static/index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await webrtc_server.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await webrtc_server.handle_message(websocket, data)
    except WebSocketDisconnect:
        webrtc_server.disconnect(websocket)

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    return FileResponse(f"audio/{filename}")
