import os
from web3 import Web3
from eth_account import Account


def derive_pkey(ens_name: str) -> str:
    seed = os.environ["SECRET_SEED"]
    raw = Web3.keccak(text=seed + ens_name)
    return raw.hex()


def derive_wallet(ens_name: str) -> str:
    return Account.from_key(derive_pkey(ens_name)).address
