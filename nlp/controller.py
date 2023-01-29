import json
from pathlib import Path
from typing import Any

from transformers import pipeline

NLP_ROOT = Path(__file__).parent


class NLPTaskController:
    def __init__(self, task: str = "sentiment-analysis", model: str = "roberta"):
        model_config = self.load_model(task, model)
        self.pipeline = pipeline(task, model=model_config["model"])
        self.label_map = model_config["label_map"]

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

    def predict(self, text: str) -> bytes:
        prediction = self.pipeline(text)[0]
        prediction["label"] = self.label_map[prediction["label"]]
        pred_data = json.dumps(prediction, ensure_ascii=False)
        pred_data_bytes = pred_data.encode("utf-8")

        return pred_data_bytes

    def __call__(self, message: bytes, **kwargs) -> bytes:  # type: ignore[no-untyped-def]
        message_text = message.decode("utf-8")
        prediction = self.predict(message_text)
        return prediction


if __name__ == "__main__":
    controller = NLPTaskController()
    pred = controller.predict("Shut up you Malfoy")
    print(pred)
