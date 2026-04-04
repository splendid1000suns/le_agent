# Backend Architecture — FE Reference

## Stack
- FastAPI + SQLAlchemy (async) + PostgreSQL
- Run: `uvicorn main:app --reload` from `backend/`
- Docs: `GET /docs` or `GET /openapi.json`

---

## Current Endpoints

### Agents
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/agents` | Create agent |
| `GET` | `/agents/{name}` | Get agent by name |
| `GET` | `/agents?owner=<owner>` | Get all agents for an owner |

**POST /agents body:**
```json
{
  "name": "my-agent",
  "owner": "0xUserAddress",
  "strategy_prompt": "Trade USDC for WBTC when...",
  "pkey": "session_private_key",
  "image_uri": null,
  "active": true
}
```

**Agent response shape:**
```json
{
  "name": "my-agent",
  "owner": "0xUserAddress",
  "strategy_prompt": "...",
  "image_uri": null,
  "active": true
}
```

---

## Coming Soon

### Endpoint changes
- Agent identity will switch from `name` to `(user_address, ens_node)` pair
- `owner` field becomes `user_address` (Ethereum address)
- Full CRUD: `PUT` to update strategy/policy, `DELETE` to revoke

### New endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/agents/{ens_node}/start` | Start agent trading loop |
| `POST` | `/agents/{ens_node}/stop` | Stop agent trading loop |
| `GET` | `/agents/{ens_node}/logs` | LLM reasoning + trade history |
| `GET` | `/agents/{ens_node}/pnl` | Current PnL stats |
| `GET` | `/approvals/pending/{user_address}` | Pending Ledger approval requests |
| `POST` | `/approvals/{id}/submit` | Submit signed tx after Ledger confirm |
| `POST` | `/approvals/{id}/reject` | User rejected on device |
| `GET` | `/prices` | All token prices (Chainlink) |
| `GET` | `/prices/{token}` | Single token price |

### No WebSockets — use polling
- Poll `GET /approvals/pending/{user_address}` every 2-3s to detect pending Ledger approvals
- Poll `GET /agents/{ens_node}/pnl` every 30s for dashboard updates
- On approval detected → redirect to `/approve`

---

## Internal (not FE-facing)
- `AgentRunner` — per-agent asyncio loop managing trade execution
- `LLMDecider` — calls Claude API with strategy prompt + market data, returns trade decision
- `ContractClient` — calls `execute()` on PolicyContract via session key
- `UniswapBuilder` — constructs Uniswap v4 swap calldata
