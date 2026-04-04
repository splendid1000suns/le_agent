import asyncio
import logging

from utils.brain import decide
from utils.ens import get_subname
from utils.uniswap import execute_swap

logger = logging.getLogger(__name__)

# ens_name -> running asyncio Task
_runners: dict[str, asyncio.Task] = {}

LOOP_INTERVAL = 60  # seconds between each agent decision


async def _run_agent(ens_name: str) -> None:
    logger.info(f"[{ens_name}] runner started")
    while True:
        try:
            agent = await get_subname(ens_name)
            if not agent:
                logger.warning(f"[{ens_name}] agent not found in ENS, stopping")
                break

            strategy = agent["strategy"]
            policy = agent.get("policy") or {}
            tokens = policy.get("tokens", [])
            contracts = policy.get("contracts", [])

            if not tokens or not contracts:
                logger.info(f"[{ens_name}] no tokens or contracts in policy, holding")
                await asyncio.sleep(LOOP_INTERVAL)
                continue

            # Fetch prices for whitelisted tokens
            prices = await _get_prices(tokens)

            # Ask Claude to decide
            logger.info(f"[{ens_name}] thinking...")
            decision = await decide(strategy, prices, policy)
            logger.info(f"[{ens_name}] decision: {decision['action']} — {decision['reasoning']}")

            if decision["action"] == "swap" and decision["amount_usd"] > 0:
                token_in = decision["token_in"]
                token_out = decision["token_out"]
                amount_usd = decision["amount_usd"]
                router = contracts[0]

                # Convert USD amount to wei using token_in price
                price_in = prices.get(token_in.lower(), 0)
                if price_in <= 0:
                    logger.warning(f"[{ens_name}] no price for token_in {token_in}, skipping")
                    await asyncio.sleep(LOOP_INTERVAL)
                    continue

                # Assume 18 decimals — adjust per token in prod
                amount_in_wei = int((amount_usd / price_in) * 10**18)

                logger.info(f"[{ens_name}] swapping {amount_usd} USD of {token_in} → {token_out}")
                tx_hash = execute_swap(
                    ens_name=ens_name,
                    token_in=token_in,
                    token_out=token_out,
                    amount_in_wei=amount_in_wei,
                    router=router,
                )
                logger.info(f"[{ens_name}] tx sent: {tx_hash}")

        except asyncio.CancelledError:
            logger.info(f"[{ens_name}] runner cancelled")
            break
        except Exception as e:
            logger.error(f"[{ens_name}] error: {e}")

        await asyncio.sleep(LOOP_INTERVAL)


async def _get_prices(token_addresses: list[str]) -> dict[str, float]:
    """Fetch USD prices from CoinGecko for a list of token addresses."""
    import httpx

    if not token_addresses:
        return {}

    addresses = ",".join(a.lower() for a in token_addresses)
    url = (
        "https://api.coingecko.com/api/v3/simple/token_price/ethereum"
        f"?contract_addresses={addresses}&vs_currencies=usd"
    )
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.get(url)
        data = res.json()
        return {addr: info["usd"] for addr, info in data.items() if "usd" in info}
    except Exception as e:
        logger.error(f"price fetch failed: {e}")
        return {}


def start_runner(ens_name: str) -> None:
    if ens_name in _runners:
        return
    task = asyncio.create_task(_run_agent(ens_name))
    _runners[ens_name] = task


def stop_runner(ens_name: str) -> None:
    task = _runners.pop(ens_name, None)
    if task:
        task.cancel()


def start_all(ens_names: list[str]) -> None:
    for ens_name in ens_names:
        start_runner(ens_name)


def stop_all() -> None:
    for ens_name in list(_runners):
        stop_runner(ens_name)


def is_running(ens_name: str) -> bool:
    return ens_name in _runners
