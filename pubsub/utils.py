import json
from pathlib import Path
from typing import Union, Any, Dict


def read_json(filepath: Union[str, Path]) -> Dict[str, Any]:
    assert str(filepath).endswith(".json")
    
    with open(filepath, "r", encoding="utf-8") as f:
        json_data = json.load(f)
    
    return json_data


def get_project_root() -> Path:
    root_dir = Path(__file__).absolute().parent.parent
    assert str(root_dir).endswith("need-base")
    
    return root_dir
