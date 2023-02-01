import os
import json
from tempfile import NamedTemporaryFile
from pathlib import Path
from typing import Any

from transformers import pipeline

from needpubsub.subscribe import subscribe_message_async
from needpubsub.publish import publish_message

NLP_ROOT = Path(__file__).parent


class STTController:
    task = "automatic-speech-recognition"
    
    def __init__(
        self,
        model: str = "wav2vec2-large",
        project_id: str = "iitp-class-team-4",
        topic_id: str = "stt-text"
    ):
        self.project_id = project_id
        self.topic_id = topic_id
        model_name = self.load_model(model)
        self.pipeline = pipeline(self.task, model=model_name)

    def load_model(self, model: str) -> Any:
        with open(NLP_ROOT / "model_card.json", "r", encoding="utf-8") as f:
            model_card = json.load(f)
        model_name = model_card[self.task].get(model)
        if model_name is None:
            raise ValueError(f"Model {model} not supported for task {self.task}")

        return model_name
    
    def inference(self, audio: bytes) -> bytes:
        with NamedTemporaryFile(suffix=".wav", delete=False) as fp:
            fp.write(audio)
            temp_audio_name = fp.name
        
        prediction = self.pipeline(temp_audio_name)["text"].lower()
        prediction_bytes = prediction.encode("utf-8")
        
        os.remove(temp_audio_name)
        
        return prediction_bytes

    def eventsub(self, subscription_id: str) -> None:
        subscribe_message_async(self.project_id, subscription_id, self.sub_callback)

    def sub_callback(self, message: bytes, **kwargs) -> None:  # type: ignore[no-untyped-def]
        prediction = self.inference(message)
        device_id = kwargs.get("device_id")
        session_id = kwargs.get("session_id")
        
        print(f"Publishing {prediction.decode('utf-8')}")
        
        publish_message(
            prediction,
            project_id=self.project_id,
            topic_id=self.topic_id,
            ordering_key=device_id,
            device_id=device_id,
            session_id=session_id,
        )
        publish_message(
            prediction,
            project_id=self.project_id,
            topic_id="collector",
            device_id=device_id,
            session_id=session_id,
            data_type="text"
        )


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", type=str, help="NLP model for task in model card")
    parser.add_argument("-p", "--project_id", type=str, help="Google Pub/Sub Project ID")
    parser.add_argument("-s", "--subscription_id", type=str, help="Google Pub/Sub subscription ID")
    parser.add_argument("--topic_id", type=str, help="Google Pub/Sub Topic ID")
    args = parser.parse_args()
    
    controller = STTController(args.model, project_id=args.project_id, topic_id=args.topic_id)
    controller.eventsub(args.subscription_id)
