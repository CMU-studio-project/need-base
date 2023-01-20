import json
from pathlib import Path
from typing import Any, Dict, Optional, Union

import rsa
from rsa.pkcs1 import DecryptionError


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


def decrypt_message(message: bytes) -> Optional[bytes]:
    priv_key_path = get_project_root() / "credentials/need-private.pem"
    with open(priv_key_path, "rb") as priv_f:
        priv_key = rsa.PrivateKey.load_pkcs1(priv_f.read())

    try:
        decrypted_message = rsa.decrypt(message, priv_key=priv_key)
        return decrypted_message
    except DecryptionError:
        return None
