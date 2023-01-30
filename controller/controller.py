import os
import time

from pubsub.publish import publish_message
from pubsub.pull_subscribe import subscribe_message


class MainController:
    def __init__(self) -> None:
        self.device_id = os.environ["NEED_PROJECT_DEVICE_ID"]  # pi7 / pi8
        self.text_topic_id = "mic_text"

    def listen(self) -> None:
        """Mic Listener"""
        return None

    def publish_text(self, text: str) -> None:
        encoded_text = text.encode("utf-8")
        session_id = str(time.time_ns())
        publish_message(
            encoded_text,
            self.text_topic_id,
            ordering_key=self.device_id,
            device_id=self.device_id,
            session_id=session_id,
        )

    def get_response(self) -> None:
        subscription_id = f"sentiment-{self.device_id}-sub"
        subscribe_message(subscription_id, timeout=5)

    def run_task(self, text: str) -> None:
        self.publish_text(text)
        self.get_response()


if __name__ == "__main__":
    ctrl = MainController()
    while True:
        t0 = time.time()
        ctrl.run_task("Shut up Malfoy")
        t1 = time.time()
        print(f"Time: {t1 - t0:.3f}")