import google.generativeai as genai
import os

class AIReplyGenerator:
    def __init__(self, api_key=None):
        """
        Initialize AI reply generator
        api_key: Your Google Gemini API key (or set GEMINI_API_KEY env variable)
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key required. Set GEMINI_API_KEY env variable or pass api_key parameter")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        # Customize this prompt to match your personality
        self.system_prompt = """You are responding as a League of Legends player who is currently busy but wants to stay friendly with friends.

Your personality:
- Casual and friendly Vietnamese gamer
- Currently busy with something but polite
- Keep responses short (1-2 sentences max)
- Use casual Vietnamese mixed with gaming terms
- Sometimes use "bro", "ông", "mày" depending on context

Examples of your style:
- "Đang bận bro, hẹn sau nhé"
- "5 phút nữa xong, đợi tí"
- "Đang làm việc nè, chiều chơi"
- "Bận rồi ông, hẹn tối"

Keep it natural and vary your responses. Don't always say the exact same thing."""

        self.conversation_history = {}
        self.chat_sessions = {}  # Store Gemini chat sessions per conversation

    def generate_reply(self, friend_name, message, conversation_id):
        """
        Generate AI reply based on friend's message
        """
        # Initialize chat session if new conversation
        if conversation_id not in self.chat_sessions:
            self.chat_sessions[conversation_id] = self.model.start_chat(history=[])
            self.conversation_history[conversation_id] = []
        
        # Add friend's message to history for tracking
        self.conversation_history[conversation_id].append({
            "friend": friend_name,
            "message": message
        })
        
        # Keep only last 10 messages to avoid token limits
        if len(self.conversation_history[conversation_id]) > 10:
            self.conversation_history[conversation_id] = self.conversation_history[conversation_id][-10:]
            # Reset chat session if history gets too long
            self.chat_sessions[conversation_id] = self.model.start_chat(history=[])
        
        try:
            # Create prompt with system instructions
            prompt = f"""{self.system_prompt}

Friend {friend_name} says: {message}

Your response (keep it short, 1-2 sentences max):"""
            
            response = self.chat_sessions[conversation_id].send_message(prompt)
            reply = response.text.strip()
            
            return reply
            
        except Exception as e:
            print(f"[AI ERROR] {e}")
            # Fallback response if AI fails
            return "Đang bận bro, hẹn sau nhé"