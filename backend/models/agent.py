from pydantic import BaseModel

from models.policy import Policy


class AgentCreate(BaseModel):
    name: str
    description: str | None = None
    image_uri: str | None = None
    strategy_type: str  # "PRICE_ACTION" | "POLYMARKET" | "X_SENTIMENT"
    strategy_prompt: str
    policy: Policy


class AgentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    image_uri: str | None = None
    strategy_type: str | None = None
    strategy_prompt: str | None = None
    policy: Policy | None = None
    active: bool | None = None


class AgentResponse(BaseModel):
    id: int
    owner: str
    name: str
    description: str | None
    image_uri: str | None
    strategy_type: str
    strategy_prompt: str
    active: bool
    status: dict | None
    policy: Policy | None

    model_config = {"from_attributes": True}
