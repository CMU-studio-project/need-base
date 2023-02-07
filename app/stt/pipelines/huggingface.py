import os
from tempfile import NamedTemporaryFile
from transformers import pipeline

class HuggingfacePipeline:
    task = "automatic-speech-recognition"
    
    def __init__(self, model):
        self.pipeline = pipeline(self.task, model=model)
        
    def inference(self, audio: bytes, extension: str):
        with NamedTemporaryFile(suffix=extension, delete=False) as fp:
            fp.write(audio)
            temp_audio_name = fp.name

        prediction = self.pipeline(temp_audio_name)["text"].lower()
        os.remove(temp_audio_name)
        
        return {
            "transcript": prediction,
            "confidence": None,
            "language": "en-US"
        }
    
    def __call__(self, audio: bytes, extension: str):
        return self.inference(audio, extension)