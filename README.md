# League of Legends Auto-Reply Bot with AI

An intelligent auto-reply bot for League of Legends client that uses Google Gemini AI to generate natural responses to your friends' messages.

## Features

✅ **Smart Friend Detection**: Only replies to messages from friends, not your own messages  
✅ **Account Name Mapping**: Shows friend names instead of conversation IDs  
✅ **AI-Powered Responses**: Uses Google Gemini AI to generate natural, contextual replies  
✅ **Fast Response Time**: 4-5 second cooldown between replies  
✅ **Conversation History**: AI maintains context across multiple messages  
✅ **Fallback Mode**: Works without AI with simple pre-set replies  

## Requirements

- Python 3.8+
- League of Legends Client running
- Google Gemini API key (for AI features)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your Gemini API key:
```bash
# Windows
set GEMINI_API_KEY=your_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_api_key_here
```

Or enter it when prompted when running the bot.

## Getting Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

## Usage

1. Start League of Legends client and log in
2. Run the bot:
```bash
python main.py
```

3. The bot will:
   - Connect to League Client
   - Show your logged-in account
   - Start monitoring messages
   - Auto-reply to friends with AI-generated responses

## Customization

### Adjust Reply Interval

In `auto_reply.py`, change:
```python
COOLDOWN_SECONDS = 5  # Change to 4-10 seconds as needed
```

### Customize AI Personality

In `ai_reply.py`, edit the `system_prompt` to match your style:
```python
self.system_prompt = """You are responding as a League of Legends player...
Your personality:
- Add your personality traits here
- Customize response style
- Add preferred phrases
"""
```

### Simple Reply Mode (Without AI)

If you don't provide an API key, the bot will use a simple reply:
```python
reply = "Đang bận, 5 phút nữa chơi"
```

You can change this in `auto_reply.py` in the `on_message` method.

## How It Works

1. **LCU Connection**: Connects to League Client via WebSocket API
2. **Message Detection**: Monitors incoming chat messages
3. **Friend Filtering**: Checks if message is from a friend (not from you)
4. **Name Resolution**: Maps conversation IDs to friend names
5. **AI Response**: Generates contextual reply using Claude AI
6. **Send Reply**: Sends message back through LCU API

## Troubleshooting

**Bot not starting:**
- Make sure League Client is running
- Check if you have admin privileges (may be required)

**No AI responses:**
- Verify your API key is correct
- Check your internet connection
- Bot will fall back to simple replies if AI fails

**Not replying to messages:**
- Check cooldown settings (may need to wait 5 seconds)
- Verify message is from a friend, not from you
- Check console for error messages

## File Structure

- `main.py` - Entry point, handles setup
- `auto_reply.py` - Main bot logic and message handling
- `lcu_auth.py` - League Client authentication
- `lcu_chat.py` - Chat API functions
- `ai_reply.py` - AI response generation
- `requirements.txt` - Python dependencies

## API Usage

This bot uses the Google Gemini API. The free tier includes:
- 60 requests per minute
- Generous token limits
- Check [Gemini API pricing](https://ai.google.dev/pricing) for current rates

## Safety Notes

- Bot only reads/sends chat messages, doesn't interact with game
- All communication is local (League Client on your machine)
- API key is never shared or logged
- You can stop the bot anytime with Ctrl+C

## License

MIT License - Feel free to modify and use as needed!