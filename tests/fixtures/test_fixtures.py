from sqlalchemy.ext.asyncio import AsyncSession

from tests.testing_tools.utils import assert_isinstance


def test__init_db_fixture(init_db):
    assert init_db is None


def test__get_test_session_fixture(get_test_session):
    assert_isinstance(get_test_session, AsyncSession)


# import asyncio
#
# async def test__provided_loop_is_running_loop(
#     event_loop: asyncio.AbstractEventLoop,
# ) -> None:
#     assert event_loop is asyncio.get_running_loop()
