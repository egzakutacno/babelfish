from aiortc import RTCPeerConnection, MediaStreamTrack
import json

class WebRTCServer:
    def __init__(self):
        self.clients = {}

    async def connect(self, websocket):
        self.clients[websocket] = RTCPeerConnection()

    async def disconnect(self, websocket):
        if websocket in self.clients:
            await self.clients[websocket].close()
            del self.clients[websocket]

    async def handle_message(self, websocket, message):
        data = json.loads(message)
        pc = self.clients[websocket]

        if data["type"] == "offer":
            await pc.setRemoteDescription(data["offer"])
            answer = await pc.createAnswer()
            await pc.setLocalDescription(answer)
            await websocket.send_text(json.dumps({"type": "answer", "answer": pc.localDescription}))
        elif data["type"] == "candidate":
            candidate = data["candidate"]
            await pc.addIceCandidate(candidate)
