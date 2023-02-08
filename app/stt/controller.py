import json
from pathlib import Path
from typing import Any

from needpubsub.publish import publish_message

from app.base import BaseController
from app.stt.pipelines import GoogleCloudPipeline, HuggingfacePipeline


class STTController(BaseController):
    task = "automatic-speech-recognition"

    def __init__(
        self,
        model: str = "wav2vec2-large",
        project_id: str = "iitp-class-team-4",
        topic_id: str = "stt-text",
    ):
        super(STTController, self).__init__(project_id)
        self.topic_id = topic_id
        model_name = self.load_model(model)
        print(f"Loading model {model_name}...")

        self.pipeline = self.load_pipeline(model_name)
        self.data_type = "phoneme" if "phoneme" in model else "text"

    def load_model(self, model: str) -> Any:
        with open(Path(__file__).parent / "model_card.json", "r", encoding="utf-8") as f:
            model_card = json.load(f)
        model_name = model_card[self.task].get(model)
        if model_name is None:
            raise ValueError(f"Model {model} not supported for task {self.task}")

        return model_name

    def load_pipeline(self, model_name: str) -> Any:
        if model_name == "google-cloud":
            pipeline = GoogleCloudPipeline()
        else:
            pipeline = HuggingfacePipeline(model=model_name)
        return pipeline

    def inference(self, audio: bytes, extension: str = "wav") -> bytes:
        prediction = self.pipeline(audio, extension)
        prediction_bytes = json.dumps(prediction, ensure_ascii=False).encode("utf-8")

        return prediction_bytes

    def handle_callback(self, message: bytes, **kwargs) -> None:  # type: ignore[no-untyped-def]
        extension = kwargs.get("audio_ext", "wav")
        prediction = self.inference(message, extension)
        device_id = kwargs.get("device_id")

        print(f"Publishing {prediction.decode('utf-8')}", flush=True)

        if self.data_type == "text":
            publish_message(
                prediction,
                project_id=self.project_id,
                topic_id=self.topic_id,
                ordering_key=device_id,
                **kwargs,
            )

        publish_message(
            prediction,
            project_id=self.project_id,
            topic_id="collector",
            data_type=self.data_type,
            **kwargs,
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", type=str, help="NLP model for task in model card")
    parser.add_argument("-p", "--project_id", type=str, help="Google Pub/Sub Project ID")
    parser.add_argument("-s", "--subscription_id", type=str, help="Google Pub/Sub subscription ID")
    parser.add_argument("--topic_id", type=str, help="Google Pub/Sub Topic IDs")
    args = parser.parse_args()

    controller = STTController(args.model, project_id=args.project_id, topic_id=args.topic_id)
    controller.eventsub(args.subscription_id)
