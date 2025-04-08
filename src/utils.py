import asyncio


async def delay(coro, seconds: int) -> None:
    await asyncio.sleep(seconds)
    await coro


def delay_task(coro, seconds: int) -> asyncio.Task:
    return asyncio.create_task(delay(coro, seconds))
