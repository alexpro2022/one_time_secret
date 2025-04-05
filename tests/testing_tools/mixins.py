from httpx import Response

from src.repo.models import Base
from src.types_app import _AS, _F
from tests.testing_tools.utils import assert_equal, assert_isinstance


class DBMixin:
    db_save_obj: _F | None = None  # type: ignore [valid-type]
    model = None
    """Model is necessary for check_db if db_save_obj is None. Usualyy it is to test the creation."""
    db_vs_response: bool = False
    db_delete_action: bool = False

    async def setup_db(self, session: _AS) -> None:
        if self.db_save_obj is not None:
            self.obj = self.db_save_obj()
            session.add(self.obj)
            await session.commit()
            self.model = self.obj.__class__

    async def check_db(self, session: _AS, response: Response) -> None:
        assert_isinstance(response, Response)
        if self.db_vs_response:
            if self.model is None:
                raise NotImplementedError("No model for DB checking.")
            from_db = await session.get(self.model, response.json().get("id"))
            if self.db_delete_action:
                assert from_db is None
            else:
                assert from_db is not None
                assert_isinstance(from_db, Base)
                await session.refresh(from_db)
                db_json = from_db.model_dump()
                db_json["id"] = str(db_json["id"])
                assert_equal(db_json, response.json())


async def setup_db(obj, session: _AS):
    if hasattr(obj, "setup_db"):
        await obj.setup_db(session)


async def check_db(obj, session: _AS, response: Response):
    if hasattr(obj, "check_db"):
        await obj.check_db(session, response)


# async def check_db(
#     *,
#     session: _AS,
#     model: TypeModel,
#     response: Response,
#     delete: bool = False,
# ) -> None:
#     assert_isinstance(response, Response)
#     obj = await session.get(model, response.json().get("id"))
#     if delete:
#         assert obj is None
#     else:
#         assert obj is not None
#         await session.refresh(obj)
#         db_json = obj.model_dump()
#         db_json["id"] = str(db_json["id"])
#         assert_equal(db_json, response.json())
