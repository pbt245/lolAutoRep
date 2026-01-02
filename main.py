from lcu_auth import get_lcu_credentials
from auto_reply import AutoReplyBot

def main():
    port, token = get_lcu_credentials()
    bot = AutoReplyBot(port, token)
    bot.run()

if __name__ == "__main__":
    main()
