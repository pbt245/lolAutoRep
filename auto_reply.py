import websocket
import ssl
import json
import time
import base64

from lcu_chat import send_message, get_current_summoner, get_conversation_info
from ai_reply import AIReplyGenerator

COOLDOWN_SECONDS = 5  # Reduced to 4-5 seconds

class AutoReplyBot:
    def __init__(self, port, token, ai_api_key=None):
        self.port = port
        self.token = token
        self.last_replied = {}
        self.my_puuid = None
        self.my_name = None
        self.conversation_names = {}  # Map conversation_id -> friend_name
        
        # Initialize AI
        try:
            self.ai_generator = AIReplyGenerator(api_key=ai_api_key)
            self.use_ai = True
            print("[AI] AI reply generator initialized")
        except Exception as e:
            print(f"[AI] Failed to initialize AI: {e}")
            print("[AI] Falling back to simple replies")
            self.ai_generator = None
            self.use_ai = False
        
        # Get current user info
        self._init_current_user()

    def _init_current_user(self):
        """Get current logged-in user information"""
        try:
            self.my_puuid, self.my_name, game_tag = get_current_summoner(self.port, self.token)
            if self.my_name:
                print(f"[INFO] Logged in as: {self.my_name}#{game_tag if game_tag else ''}")
                print(f"[INFO] Your PUUID: {self.my_puuid}")
            else:
                print("[WARN] Could not get current user info")
        except Exception as e:
            print(f"[ERROR] Failed to get current user: {e}")

    def _get_friend_name(self, conversation_id):
        """Get or fetch friend name for a conversation"""
        if conversation_id in self.conversation_names:
            return self.conversation_names[conversation_id]
        
        try:
            name, game_tag = get_conversation_info(self.port, self.token, conversation_id)
            if name:
                full_name = f"{name}#{game_tag}" if game_tag else name
                self.conversation_names[conversation_id] = full_name
                return full_name
        except Exception as e:
            print(f"[WARN] Could not get name for {conversation_id}: {e}")
        
        return "Friend"

    def on_open(self, ws):
        ws.send(json.dumps([5, "OnJsonApiEvent"]))
        print("[STATUS] Auto-reply bot is running...")
        print(f"[CONFIG] Reply cooldown: {COOLDOWN_SECONDS} seconds")
        print(f"[CONFIG] AI mode: {'Enabled' if self.use_ai else 'Disabled'}")

    def on_message(self, ws, message):
        if not message:
            return

        try:
            event = json.loads(message)
        except json.JSONDecodeError:
            return

        if not isinstance(event, list) or len(event) < 3:
            return

        payload = event[2]

        uri = payload.get("uri", "")
        if not uri.startswith("/lol-chat/v1/conversations"):
            return

        data = payload.get("data")
        if not data or "lastMessage" not in data:
            return

        conversation_id = data["id"]
        last_message = data["lastMessage"]
        
        msg_body = last_message.get("body", "")
        msg_from_puuid = last_message.get("fromSummonerId") or last_message.get("fromId")
        
        # Skip if message is from me
        if self.my_puuid and msg_from_puuid == self.my_puuid:
            return
        
        # Check if message type is not a chat message (skip system messages)
        msg_type = last_message.get("type", "")
        if msg_type != "chat":
            return

        # Cooldown check
        now = time.time()
        if conversation_id in self.last_replied:
            elapsed = now - self.last_replied[conversation_id]
            if elapsed < COOLDOWN_SECONDS:
                return

        # Get friend name
        friend_name = self._get_friend_name(conversation_id)
        
        print(f"[MESSAGE] {friend_name}: {msg_body}")

        # Generate reply
        if self.use_ai and self.ai_generator:
            try:
                reply = self.ai_generator.generate_reply(friend_name, msg_body, conversation_id)
                print(f"[AI REPLY] → {friend_name}: {reply}")
            except Exception as e:
                print(f"[AI ERROR] {e}")
                reply = "Đang bận bro, hẹn sau nhé"
        else:
            # Fallback simple reply
            reply = "Đang bận, 5 phút nữa chơi"

        # Send reply
        send_message(self.port, self.token, conversation_id, reply)
        self.last_replied[conversation_id] = now

    def on_error(self, ws, error):
        print(f"[ERROR] WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print(f"[STATUS] WebSocket closed: {close_status_code} - {close_msg}")

    def run(self):
        auth = base64.b64encode(f"riot:{self.token}".encode()).decode()

        ws = websocket.WebSocketApp(
            f"wss://127.0.0.1:{self.port}/",
            header={"Authorization": f"Basic {auth}"},
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})