import base64
import json
import logging
from typing import Tuple
import os

from flask import Flask, request

from pubsub.utils import decrypt_message, get_project_root, load_task_module

app = Flask(__name__)
PROJECT_ROOT = get_project_root()

logger = logging.getLogger("subscriber-log")
logger.setLevel(logging.DEBUG)

CALLBACK_MODULE = os.environ["NEED_PROJECT_CALLBACK_MODULE"]
CALLBACK_TASK = os.environ["NEED_PROJECT_CALLBACK_TASK"]
CALLBACK_MODEL = os.environ["NEED_PROJECT_CALLBACK_MODEL"]

task_controller = load_task_module(CALLBACK_MODULE, CALLBACK_TASK, CALLBACK_MODEL)

@app.route("/", methods=["POST"])
def receive_sub() -> Tuple[str, int]:
    envelope = json.loads(request.data.decode("utf-8"))
    env_body = envelope["message"]

    # Message
    message = base64.b64decode(env_body["data"])
    decrypted_message = decrypt_message(message)
    if decrypted_message is None:
        return "Invalid message", 400

    # Attributes
    rec_data = {
        **env_body.get("attributes", {}),
        "message": decrypted_message,
        "message_id": env_body["message_id"],
    }
    task_controller(**rec_data)

    return "OK", 200


if __name__ == "__main__":
    app.run(port=18080, debug=True)
