from fastapi import APIRouter, Depends, HTTPException

from api.auth import get_current_user
from db.crud import create_agent, delete_agent, get_agent_by_id, get_agents_by_owner, get_trades_by_agent, get_trades_by_owner, update_agent
from db.database import get_db
from models.agent import AgentCreate, AgentResponse, AgentUpdate
from models.trade import TradeResponse

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("", response_model=AgentResponse, status_code=201)
async def create(body: AgentCreate, user: str = Depends(get_current_user)):
    async with get_db() as db:
        return await create_agent(db, body, owner=user)


@router.get("", response_model=list[AgentResponse])
async def get_all(user: str = Depends(get_current_user)):
    async with get_db() as db:
        return await get_agents_by_owner(db, user)


@router.get("/trades", response_model=list[TradeResponse])
async def get_all_trades(user: str = Depends(get_current_user)):
    async with get_db() as db:
        return await get_trades_by_owner(db, user)


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_by_id(agent_id: int, user: str = Depends(get_current_user)):
    async with get_db() as db:
        agent = await get_agent_by_id(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent.owner != user:
        raise HTTPException(status_code=403, detail="Forbidden")
    return agent


@router.patch("/{agent_id}", response_model=AgentResponse)
async def update(agent_id: int, body: AgentUpdate, user: str = Depends(get_current_user)):
    async with get_db() as db:
        agent = await get_agent_by_id(db, agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        if agent.owner != user:
            raise HTTPException(status_code=403, detail="Forbidden")
        return await update_agent(db, agent, body)


@router.delete("/{agent_id}", status_code=204)
async def delete(agent_id: int, user: str = Depends(get_current_user)):
    async with get_db() as db:
        agent = await get_agent_by_id(db, agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        if agent.owner != user:
            raise HTTPException(status_code=403, detail="Forbidden")
        await delete_agent(db, agent)


@router.get("/{agent_id}/trades", response_model=list[TradeResponse])
async def get_agent_trades(agent_id: int, user: str = Depends(get_current_user)):
    async with get_db() as db:
        agent = await get_agent_by_id(db, agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        if agent.owner != user:
            raise HTTPException(status_code=403, detail="Forbidden")
        return await get_trades_by_agent(db, agent_id)
