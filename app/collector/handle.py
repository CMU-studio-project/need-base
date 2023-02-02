from typing import Any, Dict
from jiwer import wer, cer

class DataHandler:
    def __init__(self):
        self.multi_session_dict = dict()
        
    @staticmethod
    def _word_match(ref: str, pred: str, threshold: float = 0.2):
        return wer(ref, pred) < threshold

    @staticmethod
    def _chr_match(ref: str, pred: str, threshold: float = 0.2):
        return cer(ref, pred) < threshold
    
    def handle(self, complete_data: Dict[str, Any]) -> Dict[str, Any]:
        text = complete_data["text"]
        sentiment = complete_data["sentiment"]
        
        command = {
            "power": None,
            "color": None,
            "intensity": None,
        }
        # check turn on
        if self._chr_match("turn on", text) or self._chr_match("lumos", text):
            command["power"] = "on"
        
        # check turn off
        elif self._chr_match("turn off", text) or self._chr_match("nox", text):
            command["power"] = "off"
            
        # check sentiment
        sentiment_label = sentiment["label"]
        if sentiment_label == "positive":
            command["color"] = [240, 100.0, 62.7]
            command["intensity"] = 100
        elif sentiment_label == "neutral":
            command["color"] = [38, 68.1, 92.2]
            command["intensity"] = 60
        elif sentiment_label == "negative":
            command["color"] = [0, 92.9, 49.8]
            command["intensity"] = 20
            
        return command
