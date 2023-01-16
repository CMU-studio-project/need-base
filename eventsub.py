from flask import Flask, request
import time
import threading
import json
import base64
import rsa
from rsa.pkcs1 import DecryptionError
import logging

from pubsub.utils import get_project_root

app = Flask(__name__)
PROJECT_ROOT = get_project_root()
PRIV_KEY_PATH = PROJECT_ROOT / "credentials/need-private.pem"

logger = logging.getLogger("subscriber-log")
logger.setLevel(logging.DEBUG)

@app.route("/", methods=["POST"])
def receive_sub():
    with open(PRIV_KEY_PATH, "rb") as priv_f:
        priv_key = rsa.PrivateKey.load_pkcs1(priv_f.read())
    
    envelope = json.loads(request.data.decode('utf-8'))
    env_body = envelope["message"]
    
    # Message
    message = base64.b64decode(env_body["data"])
    try:
        decrypted_message = rsa.decrypt(message, priv_key=priv_key)
    except DecryptionError:
        return "Invalid message", 400
    
    # Attributes
    rec_data = {
        **env_body.get("attributes", {}),
        "message": decrypted_message,
        "message_id": env_body["message_id"]
    }

    thread = threading.Thread(target=run_task, kwargs=rec_data)
    thread.start()
    print(envelope)
    
    return "OK", 200

def run_task(message, **kwargs):
    time.sleep(3)
    print(message)

if __name__ == "__main__":
    app.run(port=8080, debug=True)
