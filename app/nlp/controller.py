import json
from pathlib import Path
from typing import Any

from needpubsub.publish import publish_message
from transformers import pipeline

from app.base import BaseController


class NLPTaskController(BaseController):
    def __init__(
        self,
        task: str = "sentiment-analysis",
        model: str = "roberta",
        project_id: str = "iitp-class-team-4",
        topic_id: str = "stt-text",
    ):
        super(NLPTaskController, self).__init__(project_id)
        self.task = task
        self.topic_id = topic_id
        model_config = self.load_model(task, model)
        self.data_type = model_config["input_type"]
        self.pipeline = pipeline(task, model=model_config["model"])
        self.label_map = model_config.get("label_map")

    @staticmethod
    def load_model(task: str, model: str) -> Any:
        with open(Path(__file__).parent / "model_card.json", "r", encoding="utf-8") as f:
            model_card = json.load(f)
        task_card = model_card.get(task)
        if task_card is None:
            raise ValueError(f"Task {task} not supported")

        model_config = task_card.get(model)
        if model_config is None:
            raise ValueError(f"Model {model} not supported for task {task}")

        return model_config

    def inference(self, text: str) -> bytes:
        prediction = self.pipeline(text)[0]
        if self.label_map is not None:
            prediction["label"] = self.label_map[prediction["label"]]
        pred_data = json.dumps(prediction, ensure_ascii=False)
        pred_data_bytes = pred_data.encode("utf-8")

        return pred_data_bytes

    def handle_callback(self, message: bytes, **kwargs) -> None:  # type: ignore[no-untyped-def]
        message_text = message.decode("utf-8")
        print(f"Message {message_text} received", flush=True)

        prediction = self.inference(message_text)
        device_id = kwargs.get("device_id")
        session_id = kwargs.get("session_id")

        print(f"Publishing {prediction.decode('utf-8')}", flush=True)

        publish_message(
            prediction,
            project_id=self.project_id,
            topic_id=self.topic_id,
            ordering_key=device_id,
            device_id=device_id,
            session_id=session_id,
            data_type=self.task,
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--task", type=str, help="NLP task")
    parser.add_argument("-m", "--model", type=str, help="NLP model for task in model card")
    parser.add_argument("-p", "--project_id", type=str, help="Google Pub/Sub Project ID")
    parser.add_argument("-s", "--subscription_id", type=str, help="Google Pub/Sub subscription ID")
    parser.add_argument("--topic_id", type=str, help="Google Pub/Sub Topic ID")
    args = parser.parse_args()

    controller = NLPTaskController(
        args.task, args.model, project_id=args.project_id, topic_id=args.topic_id
    )
    controller.eventsub(args.subscription_id)
