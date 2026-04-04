from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel


class TradeResponse(BaseModel):
    tx_hash: str
    agent_id: int
    token_in: str
    token_out: str
    amount_in: Decimal
    amount_out: Decimal | None
    value_usd: Decimal
    timestamp: datetime | None
    success: bool | None
    tx_info: dict | None

    model_config = {"from_attributes": True}
