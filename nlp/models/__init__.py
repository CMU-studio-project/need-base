from .sentiment.roberta import SentimentRoberta
from .base import ModelBase

def load_model(task: str, model: str, *args, **kwargs) -> ModelBase:
    if task == "sentiment":
        if model == "roberta":
            loading_model = SentimentRoberta
        else:
            raise ValueError("Model not supported")
    else:
        raise ValueError("Task not supported")
    
    return loading_model(*args, **kwargs)
