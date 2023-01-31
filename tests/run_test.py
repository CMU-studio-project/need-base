import time
from pathlib import Path
from typing import Union

from needpubsub.publish import publish_message


class TestController:
    def __init__(self) -> None:
        self.device_id = "pi7"
        self.text_topic_id = "pi-speech"

    def publish_text(self, audio: bytes) -> None:
        session_id = str(time.time_ns())
        publish_message(
            audio,
            self.text_topic_id,
            ordering_key=self.device_id,
            device_id=self.device_id,
            session_id=session_id,
        )

    def get_response(self) -> None:
        subscription_id = f"sentiment-{self.device_id}-sub"

    def run_test(self, wav_path: Union[str, Path]) -> None:
        with open(wav_path, "rb") as f:
            audio = f.read()
        self.publish_text(audio)


if __name__ == "__main__":
    ctrl = TestController()
    wav_path = Path(__file__).parent / "ref_clean.wav"
    ctrl.run_test(wav_path)