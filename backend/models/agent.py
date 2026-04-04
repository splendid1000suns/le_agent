from pydantic import BaseModel

from models.policy import Policy


class AgentCreate(BaseModel):
    name: str
    description: str | None = None
    image_uri: str | None = None
    strategy: str
    policy: Policy
    record_sig: str


class AgentUpdate(BaseModel):
    description: str | None = None
    image_uri: str | None = None
    strategy: str | None = None
    policy: Policy | None = None
    record_sig: str


class AgentResponse(BaseModel):
    name: str
    ens_name: str
    owner: str
    wallet: str
    description: str | None
    image_uri: str | None
    strategy: str
    policy: Policy | None
    running: bool = False
