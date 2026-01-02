import websocket
import ssl
import json
import time
import base64

from lcu_chat import send_message

COOLDOWN_SECONDS = 300  # 5 phút

class AutoReplyBot:
    def __init__(self, port, token):
        self.port = port
        self.token = token
        self.last_replied = {}

    def on_open(self, ws):
        ws.send(json.dumps([5, "OnJsonApiEvent"]))
        print("Auto-reply bot is running...")

    def on_message(self, ws, message):
        if not message:
            return

        try:
            event = json.loads(message)
        except json.JSONDecodeError:
            return

        if not isinstance(event, list):
            return

        payload = event[2]

        uri = payload.get("uri", "")
        if not uri.startswith("/lol-chat/v1/conversations"):
            return

        data = payload.get("data")
        if not data or "lastMessage" not in data:
            return

        conversation_id = data["id"]
        msg = data["lastMessage"]["body"]

        now = time.time()
        if conversation_id in self.last_replied:
            if now - self.last_replied[conversation_id] < COOLDOWN_SECONDS:
                return

        print(f"[AUTO-REPLY] {conversation_id}: {msg}")

        send_message(
            self.port,
            self.token,
            conversation_id,
            "5 phút nữa thầy chơi"
        )

        self.last_replied[conversation_id] = now

    def run(self):
        auth = base64.b64encode(f"riot:{self.token}".encode()).decode()

        ws = websocket.WebSocketApp(
            f"wss://127.0.0.1:{self.port}/",
            header={"Authorization": f"Basic {auth}"},
            on_open=self.on_open,
            on_message=self.on_message
        )

        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})