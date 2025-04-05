from fastapi import FastAPI

from src.api.endpoints import secret
from src.config.app_config import app_conf

# from src.fastapi.api.endpoints import all routers here


# If you don't use an alembic -> uncomment below
# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
#     await service.create_db_and_tables()
#     yield


app = FastAPI(
    title=app_conf.app_title,
    description=app_conf.app_description,
    # lifespan=lifespan,
)

for router in (
    secret.router,
    # add routers here
):
    app.include_router(router)


@app.get("/healthcheck")
def healthcheck():
    return {"message": "OK"}
