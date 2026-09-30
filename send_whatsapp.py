"""Send the digest to WhatsApp via the WhatsApp Business Cloud API.

Setup (one time, all free):
  1. Create an app at developers.facebook.com and add the WhatsApp product.
  2. In WhatsApp > API Setup you get a test phone number + temporary token.
  3. Add your own number under "To" (test recipients) and verify it.
  4. In WhatsApp Manager, create a message template (e.g. "daily_briefing")
     with one body parameter {{1}}, and wait for approval.
  5. For the daily automation, generate a permanent token (System User)
     instead of the 24h temporary one.

Usage:
    python send_whatsapp.py       # reads digest.txt, needs env vars below
"""

import os
import requests

# If Meta renames/versions the Graph API, bump this to a current version.
GRAPH_VERSION = "v21.0"


def send(message):
    token = os.environ["WHATSAPP_TOKEN"]
    phone_number_id = os.environ["WHATSAPP_PHONE_NUMBER_ID"]
    recipient = os.environ["WHATSAPP_RECIPIENT"]  # your number, digits only, e.g. 14375550199
    template = os.environ.get("WHATSAPP_TEMPLATE", "daily_briefing")

    url = f"https://graph.facebook.com/{GRAPH_VERSION}/{phone_number_id}/messages"
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "template",
        "template": {
            "name": template,
            "language": {"code": "en"},
            "components": [
                {"type": "body", "parameters": [{"type": "text", "text": message}]}
            ],
        },
    }
    resp = requests.post(
        url, headers={"Authorization": f"Bearer {token}"}, json=payload, timeout=30
    )
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    with open("digest.txt") as f:
        message = f.read()
    result = send(message)
    print("Sent:", result)
