import json

from eth_account import Account
from eth_account.messages import encode_defunct
from fastapi import HTTPException


def build_record_payload(name: str, strategy: str, policy: dict, description: str | None, image_uri: str | None) -> str:
    """Canonical signable payload for all ENS text records. Must match frontend signing."""
    data = {
        "name": name,
        "strategy": strategy,
        "policy": policy,
        "description": description,
        "image_uri": image_uri,
    }
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def verify_record_sig(payload: str, signature: str, expected_address: str) -> None:
    """Raises HTTP 401 if the signature does not match the expected address."""
    try:
        msg = encode_defunct(text=payload)
        recovered = Account.recover_message(msg, signature=signature)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid record signature")

    if recovered.lower() != expected_address.lower():
        raise HTTPException(status_code=401, detail="Record signature does not match authenticated user")
