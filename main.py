import os
from lcu_auth import get_lcu_credentials
from auto_reply import AutoReplyBot

def main():
    print("=== League of Legends Auto-Reply Bot ===")
    print("Starting bot...\n")
    
    try:
        port, token = get_lcu_credentials()
        print(f"[INFO] Connected to League Client (Port: {port})\n")
    except RuntimeError as e:
        print(f"[ERROR] {e}")
        print("[ERROR] Please make sure League Client is running")
        return
    
    # Get API key from environment or prompt user
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("[INFO] No GEMINI_API_KEY found in environment")
        print("[INFO] You can either:")
        print("  1. Set environment variable: GEMINI_API_KEY=your_key")
        print("  2. Enter it now (or press Enter to skip AI features)")
        api_key = input("\nEnter your Gemini API key (or Enter to skip): ").strip()
        
        if not api_key:
            print("\n[INFO] Running without AI features (simple replies only)")
            api_key = None
        else:
            print("\n[INFO] API key provided, AI features enabled")
    
    bot = AutoReplyBot(port, token, ai_api_key=api_key)
    
    print("\n[INFO] Press Ctrl+C to stop the bot\n")
    print("="*50)
    
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n\n[INFO] Bot stopped by user")
    except Exception as e:
        print(f"\n[ERROR] Bot crashed: {e}")

if __name__ == "__main__":
    main()