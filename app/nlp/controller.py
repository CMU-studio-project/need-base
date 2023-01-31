import os
import json
from tempfile import NamedTemporaryFile
from pathlib import Path
from typing import Any

from transformers import pipeline

from needpubsub.subscribe import subscribe_message_async
from needpubsub.publish import publish_message

NLP_ROOT = Path(__file__).parent


class NLPTaskController:
    def __init__(self, task: str = "sentiment-analysis", model: str = "roberta"):
        model_config = self.load_model(task, model)
        self.data_type = model_config["input_type"]
        self.pipeline = pipeline(task, model=model_config["model"])
        self.label_map = model_config.get("label_map")

    @staticmethod
    def load_model(task: str, model: str) -> Any:
        with open(NLP_ROOT / "model_card.json", "r", encoding="utf-8") as f:
            model_card = json.load(f)
        task_card = model_card.get(task)
        if task_card is None:
            raise ValueError(f"Task {task} not supported")

        model_config = task_card.get(model)
        if model_config is None:
            raise ValueError(f"Model {model} not supported for task {task}")

        return model_config

    def text_inference(self, text: str) -> bytes:
        prediction = self.pipeline(text)[0]
        if self.label_map is not None:
            prediction["label"] = self.label_map[prediction["label"]]
        pred_data = json.dumps(prediction, ensure_ascii=False)
        pred_data_bytes = pred_data.encode("utf-8")

        return pred_data_bytes
    
    def audio_inference(self, audio: bytes) -> bytes:
        with NamedTemporaryFile(suffix=".wav", delete=False) as fp:
            fp.write(audio)
            temp_audio_name = fp.name
        
        prediction = self.pipeline(temp_audio_name)[0]
        prediction_bytes = prediction.encode("utf-8")
        
        os.remove(temp_audio_name)
        
        return prediction_bytes

    def eventsub(self, project_id: str, subscription_id: str) -> None:
        subscribe_message_async(project_id, subscription_id, self.sub_callback)

    def sub_callback(self, message: bytes, **kwargs) -> None:  # type: ignore[no-untyped-def]
        if self.data_type == "text":
            message_text = message.decode("utf-8")
            prediction = self.text_inference(message_text)
        elif self.data_type == "audio":
            prediction = self.audio_inference(message)
        else:
            raise ValueError("Unsupported data type")
        
        publish_message(prediction, ordering_key=kwargs.get("device_id"), **kwargs)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--task", type=str, help="NLP task")
    parser.add_argument("-m", "--model", type=str, help="NLP model for task in model card")
    parser.add_argument("-p", "--project_id", type=str, help="Project ID")
    parser.add_argument("-s", "--subscription_id", type=str, help="Google Pub/Sub subscription ID")
    args = parser.parse_args()
    
    controller = NLPTaskController(args.task, args.model)
    controller.eventsub(args.project_id, args.subscription_id)
