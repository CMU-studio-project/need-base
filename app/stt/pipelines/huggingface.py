import os
from tempfile import NamedTemporaryFile
from typing import Any, Dict

from transformers import pipeline


class HuggingfacePipeline:
    task = "automatic-speech-recognition"

    def __init__(self, model: str) -> None:
        self.pipeline = pipeline(self.task, model=model)

    def inference(self, audio: bytes, extension: str) -> Dict[str, Any]:
        with NamedTemporaryFile(suffix=extension, delete=False) as fp:
            fp.write(audio)
            temp_audio_name = fp.name

        prediction = self.pipeline(temp_audio_name, max_new_tokens=448)["text"].lower()
        os.remove(temp_audio_name)

        return {"transcript": prediction, "confidence": None, "language": "en-US"}

    def __call__(self, audio: bytes, extension: str) -> Dict[str, Any]:
        return self.inference(audio, extension)
