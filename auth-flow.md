# Auth Flow

Authentication is wallet-based (no passwords). The backend issues a JWT after verifying an Ethereum wallet signature.

## Steps

**1. Get a nonce**
```
GET /auth/nonce/{address}
→ { "nonce": "a3f9c2..." }
```

**2. Sign a message**
```js
const message = `Sign in nonce: ${nonce}`
const signature = await wallet.signMessage(message)
```

**3. Verify and get token**
```
POST /auth/verify
{ "address": "0x...", "message": "Sign in nonce: a3f9c2...", "signature": "0x..." }
→ { "token": "<jwt>" }
```

**4. Use the token**

Send on every protected request:
```
Authorization: Bearer <jwt>
```

## Notes
- Token expires after 24 hours — repeat the flow to get a new one
- All `/agents` endpoints are protected — requests without a valid token get `401`
- `owner` is never sent in request bodies — the backend derives it from the token
- `GET /agents` returns only the authenticated user's agents
- `GET /agents/{name}` returns `403` if the agent belongs to someone else
