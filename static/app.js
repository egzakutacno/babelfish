const ws = new WebSocket("ws://localhost:8000/ws");
const audioElement = document.getElementById("audio");

let pc = new RTCPeerConnection();

pc.ontrack = (event) => {
    audioElement.srcObject = event.streams[0];
};

ws.onmessage = async (event) => {
    const data = JSON.parse(event.data);

    if (data.type === "answer") {
        await pc.setRemoteDescription(data.answer);
    } else if (data.type === "candidate") {
        await pc.addIceCandidate(data.candidate);
    }
};

pc.onicecandidate = (event) => {
    if (event.candidate) {
        ws.send(JSON.stringify({ type: "candidate", candidate: event.candidate }));
    }
};

(async () => {
    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);

    ws.send(JSON.stringify({ type: "offer", offer: pc.localDescription }));
})();
