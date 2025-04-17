from fastapi import FastAPI
from src.config import app_config as c
from src.fastapi.api.endpoints import development, secret

app = FastAPI(
    title=c.app_conf.app_title,
    description=c.app_conf.app_description,
)

for router in (
    development.router,
    secret.router,
):
    app.include_router(router)


@app.get("/healthcheck")
def healthcheck():
    return {"message": "OK"}
