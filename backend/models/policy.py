from pydantic import BaseModel


class PolymarketTrigger(BaseModel):
    token_id: str  # polymarket token id (uint256, stored as string)
    threshold: float
    gt: bool  # polymarket odds > threshold


class Policy(BaseModel):
    tokens: list[str]  # whitelisted token addresses
    contracts: list[str]  # whitelisted contract addresses (e.g. Uniswap router)
    triggers: list[PolymarketTrigger]  # list of polymarket triggers
    rate_limit_24h: int  # max number of trades per 24h
    value_limit_24h: int  # max USD value per 24h
