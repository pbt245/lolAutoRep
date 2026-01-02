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
