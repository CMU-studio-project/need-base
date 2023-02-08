import glob
import random
import json
from pathlib import Path
import time
from typing import Union

from needpubsub.publish import publish_message
from needpubsub.subscribe import subscribe_message_sync


class TestController:
    def __init__(self) -> None:
        self.device_id = "test"
        self.text_topic_id = "pi-speech"

    def publish_text(self, audio: bytes) -> None:
        session_id = str(time.time_ns())
        publish_message(
            audio,
            "iitp-class-team-4",
            self.text_topic_id,
            ordering_key=self.device_id,
            device_id=self.device_id,
            session_id=session_id,
        )

    def get_response(self) -> None:
        subscription_id = f"command-{self.device_id}-sub"
        subscribe_message_sync("iitp-class-team-4", subscription_id, self.sub_callback)

    def run_test(self, wav_path: Union[str, Path]) -> None:
        with open(wav_path, "rb") as f:
            audio = f.read()
        self.publish_text(audio)
        self.get_response()

    @staticmethod
    def sub_callback(message: bytes, **kwargs):
        command = json.loads(message.decode("utf-8"))
        print(command)
        print(kwargs)


if __name__ == "__main__":
    ctrl = TestController()
    wav_paths = glob.glob(str(Path(__file__).parent / "spell_wav" / "*.wav"))

    times = []
    for i in range(30):
        wav_path = random.choice(wav_paths)
        print(f"Testing {wav_path}")
        
        t0 = time.time()
        ctrl.run_test(wav_path)
        t1 = time.time()
        times.append(t1 - t0)
        print(f"Time: {t1 - t0}")

    print(f"Avg time: {sum(times) / len(times):.3f}")
