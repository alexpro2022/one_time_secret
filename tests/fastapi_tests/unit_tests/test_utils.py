import pytest
from fastapi.exceptions import HTTPException

from src.api import utils
from src.repo.db import exceptions


async def coro(exception, msg):
    raise exception(msg)


async def test__try_return_not_found():
    msg = "NotFound"

    with pytest.raises(HTTPException, match=msg) as exc:
        await utils.try_return(
            return_coro=coro(exceptions.NotFound, msg),
            # exception by default == exceptions.NotFound,
            # status_code by default == 404
        )
    assert exc.value.status_code == 404


async def test__try_return_already_exists():
    msg = "AlreadyExists"
    status_code = 400

    with pytest.raises(HTTPException, match=msg) as exc:
        await utils.try_return(
            return_coro=coro(exceptions.AlreadyExists, msg),
            possible_exception=exceptions.AlreadyExists,
            raise_status_code=status_code,
        )
    assert exc.value.status_code == status_code
