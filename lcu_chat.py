import requests
import base64
import urllib3

urllib3.disable_warnings()

def send_message(port, token, conversation_id, text):
    auth = base64.b64encode(f"riot:{token}".encode()).decode()

    url = (
        f"https://127.0.0.1:{port}"
        f"/lol-chat/v1/conversations/{conversation_id}/messages"
    )

    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    }

    payload = {
        "body": text
    }

    r = requests.post(url, headers=headers, json=payload, verify=False)
    return r.status_code

def get_current_summoner(port, token):
    """Get current logged-in summoner info"""
    auth = base64.b64encode(f"riot:{token}".encode()).decode()
    
    url = f"https://127.0.0.1:{port}/lol-chat/v1/me"
    
    headers = {
        "Authorization": f"Basic {auth}"
    }
    
    r = requests.get(url, headers=headers, verify=False)
    if r.status_code == 200:
        data = r.json()
        return data.get("puuid"), data.get("gameName"), data.get("game_tag")
    return None, None, None

def get_conversation_info(port, token, conversation_id):
    """Get conversation details including participant name"""
    auth = base64.b64encode(f"riot:{token}".encode()).decode()
    
    url = f"https://127.0.0.1:{port}/lol-chat/v1/conversations/{conversation_id}"
    
    headers = {
        "Authorization": f"Basic {auth}"
    }
    
    r = requests.get(url, headers=headers, verify=False)
    if r.status_code == 200:
        data = r.json()
        # For direct messages, get the other participant's name
        if data.get("type") == "chat":
            # The name might be in different fields depending on API version
            name = data.get("name") or data.get("gameName")
            game_tag = data.get("gameTag")
            return name, game_tag
    return None, None