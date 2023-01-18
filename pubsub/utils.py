import json
from pathlib import Path
from typing import Any, Dict, Union

import rsa


def read_json(filepath: Union[str, Path]) -> Dict[str, Any]:
    assert str(filepath).endswith(".json")

    with open(filepath, "r", encoding="utf-8") as f:
        json_data = json.load(f)

    return json_data


def get_project_root() -> Path:
    return Path(__file__).absolute().parent.parent


def encrypt_message(message: bytes) -> bytes:
    public_key_path = get_project_root() / "credentials/need-public.pem"
    with open(public_key_path, "rb") as pub_f:
        pub_key = rsa.PublicKey.load_pkcs1(pub_f.read())

    encrypted_message = rsa.encrypt(message, pub_key=pub_key)
    return encrypted_message
