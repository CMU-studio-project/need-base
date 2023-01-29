import base64
import json
import logging
import os
from typing import Tuple

from flask import Flask, request

from nlp.controller import NLPTaskController
from pubsub.publish import publish_message
from pubsub.utils import decrypt_message, get_project_root

app = Flask(__name__)
PROJECT_ROOT = get_project_root()

logger = logging.getLogger("subscriber-log")
logger.setLevel(logging.DEBUG)

CALLBACK_TASK = os.environ["NEED_PROJECT_CALLBACK_TASK"]
CALLBACK_MODEL = os.environ["NEED_PROJECT_CALLBACK_MODEL"]

task_controller = NLPTaskController(CALLBACK_TASK, CALLBACK_MODEL)


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
    }
    run_task(**rec_data)

    return "OK", 200


def run_task(message: bytes, **kwargs) -> None:  # type: ignore[no-untyped-def]
    prediction = task_controller(message, **kwargs)
    device_id = kwargs.get("device_id", "")
    if device_id == "pi7":
        topic_id = "sentiment-pi7"
    elif device_id == "pi8":
        topic_id = "sentiment-pi8"
    else:
        raise ValueError("Unsupported device")
    session_id = kwargs.get("session_id", device_id)

    publish_message(
        prediction, topic_id, device_id=device_id, session_id=session_id, ordering_key=device_id
    )


if __name__ == "__main__":
    app.run(port=18080, debug=True)
