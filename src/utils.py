import asyncio
from collections.abc import Coroutine
from datetime import datetime as dt
from typing import Any


async def delay(coro, seconds: int) -> None:
    await asyncio.sleep(seconds)
    await coro


def delay_task(task_name: Any, coro: Coroutine, seconds: int) -> asyncio.Task:
    return asyncio.create_task(
        coro=delay(coro, seconds),
        name=str(task_name),
    )


def cancel_task(task_name: Any) -> bool | None:
    for task in asyncio.all_tasks():
        if task.get_name() == str(task_name):
            return task.cancel()
    return None


def get_time_now():
    return dt.now()
