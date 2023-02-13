import json
from pathlib import Path
import time
from typing import Optional, Union

from needpubsub.publish import publish_message
from needpubsub.subscribe import subscribe_message_sync


class NeedApp:
    """
    Need App Testing/Raspberry Pi app Emulator

    1. GCP에 오디오 보내서 command 받기
    2. 시간이 지나도 커맨드가 안 오면 로컬 stt+간단한 커맨드 돌리기
    2-1. 놓친 메시지 처리하기 - async로 돌리고, 해당 session 메시지만 ack?
    3. 인터넷 문제로 2도 실패하면 실패 음성 송출
    """

    def __init__(self, project_id: str, device_id: str, topic_id: str):
        self.project_id = project_id
        self.device_id = device_id
        self.topic_id = topic_id
        self.subscription_id = f"command-{self.device_id}-sub"

    def run(self, debug_audio: Optional[str] = None) -> None:
        if debug_audio is not None:
            self.send_audio(debug_audio)
            self.wait_command()

    def send_audio(self, audio: Union[bytes, Path, str], **kwargs):
        if isinstance(audio, (Path, str)):
            with open(audio, "rb") as f:
                audio_bytes = f.read()
        else:
            audio_bytes = audio

        session_id = kwargs.get("session_id", str(time.time_ns()))
        house = kwargs.get("house", None)
        house_kwargs = {"house": house} if house is not None else {}
        publish_message(
            audio_bytes,
            self.project_id,
            self.topic_id,
            device_id=self.device_id,
            session_id=session_id,
            audio_ext="wav",
            **house_kwargs,
        )

    def wait_command(self) -> None:
        subscribe_message_sync(self.project_id, self.subscription_id, self.sub_callback)

    def handle_house(self, command, **kwargs):
        house = command["house"]
        session_id = kwargs.get("session_id")

        # TODO: speaker handler로 대체
        print(f"Question for {house}: {command['speaker']}")
        # - - -

        # TODO: mic listener로 대체
        answer = input("positive/negative? ")

        answer2audio = {
            "positive": "tests/commands/positive_sentiment.wav",
            "negative": "tests/commands/negative_sentiment.wav",
        }
        answer_audio = answer2audio[answer]
        # - - -
        self.send_audio(answer_audio, session_id=session_id, house=house)
        self.wait_command()

    def sub_callback(self, message: bytes, **kwargs) -> None:
        command = json.loads(message.decode("utf-8"))
        print(command)
        print(kwargs)

        if command["house"] is not None:
            self.handle_house(command=command, **kwargs)
        else:
            print(f"Run command: {command}")


if __name__ == "__main__":
    import argparse
    import glob
    import random

    parser = argparse.ArgumentParser()
    parser.add_argument("--time_test", action="store_true", help="time test")
    parser.add_argument("--house_test", action="store_true", help="house test")

    args = parser.parse_args()

    ctrl = NeedApp(project_id="iitp-class-team-4", device_id="test", topic_id="pi-speech")

    if args.time_test:
        wav_paths = glob.glob(str(Path(__file__).parent / "spell_wav" / "*.wav"))

        times = []
        for _ in range(30):
            wav_path = random.choice(wav_paths)
            print(f"Testing {wav_path}")

            t0 = time.time()
            ctrl.run(wav_path)
            t1 = time.time()
            times.append(t1 - t0)
            print(f"Time: {t1 - t0}")

        print(f"Avg time: {sum(times) / len(times):.3f}")

    if args.house_test:
        ctrl.run("tests/commands/house_test.wav")
