from typing import Any, Dict, Tuple
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from nlp.models.base import ModelBase

class SentimentRoberta(ModelBase):
    def __init__(
            self,
            pretrained_model: str = "cardiffnlp/twitter-roberta-base-sentiment",
            device: str = "cuda:0"
    ):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.model = AutoModelForSequenceClassification.from_pretrained(pretrained_model).to(self.device)
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model)
        self.labels = ['Negative', 'Neutral', 'Positive']
        
    def encode_text(self, text: str) -> Dict[str, Any]:
        encoded = self.tokenizer(text)
        return encoded
    
    def predict_label(self, encoded_text: Dict[str, Any]) -> Tuple[str, float]:
        encoded_text = {
            key: val.to(self.device) for key, val in encoded_text.items()
        }
        
        with torch.no_grad():
            output = self.model(**encoded_text, return_dicts=True)
        
        logits = output.logits.cpu()
        pred_probs = torch.softmax(logits, dim=-1)
        max_prob, max_idx = torch.max(pred_probs, dim=-1)
        pred_label = self.labels[int(max_idx)]
        
        return pred_label, float(max_prob)
        
        
        