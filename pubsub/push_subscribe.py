import base64
import json
import logging
import threading
import time
from typing import Tuple

from flask import Flask, request

from pubsub.utils import decrypt_message, get_project_root

app = Flask(__name__)
PROJECT_ROOT = get_project_root()

logger = logging.getLogger("subscriber-log")
logger.setLevel(logging.DEBUG)


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

    thread = threading.Thread(target=run_task, kwargs=rec_data)
    thread.start()

    return "OK", 200


def run_task(message: bytes, **kwargs) -> None:  # type: ignore[no-untyped-def]
    time.sleep(3)
    print(message)

    for key, val in kwargs.items():
        print(f"{key}: {val}")


if __name__ == "__main__":
    app.run(port=8080, debug=True)
