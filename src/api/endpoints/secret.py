from fastapi import APIRouter, HTTPException, Query, status

from src.api.dependencies import secret_service, set_headers
from src.api.responses import response_400, response_404
from src.api.schemas import secret as schemas
from src.api.utils import try_return
from src.config.app_config import app_conf
from src.types_app import TypePK

router = APIRouter(
    prefix=f"{app_conf.url_prefix}/secret",
    tags=["Secrets"],
    dependencies=[set_headers],
)


@router.post(
    "",
    summary="create secret",
    description=secret_service.create.__doc__,
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.SecretKey,
)
async def create_secret(secret: secret_service, create_secret: schemas.SecretCreate):
    obj = await secret.create(**create_secret.model_dump())
    return {"secret_key": str(obj.id)}


@router.get(
    "/{secret_key}",
    summary="get secret",
    description=secret_service.get.__doc__,
    response_model=schemas.Secret,
    responses=response_404("secret"),
)
async def get_secret(secret: secret_service, secret_key: TypePK):
    obj = await try_return(return_coro=secret.get(id=secret_key))
    return {"secret": obj.secret}


@router.delete(
    "/{secret_key}",
    summary="delete secret",
    description=secret_service.delete.__doc__,
    response_model=schemas.SecretDelete,
    responses={
        **response_400("Passphrase is missing or incorrect"),
        **response_404("secret"),
    },
)
async def delete_secret(
    secret: secret_service,
    secret_key: TypePK,
    passphrase: str | None = Query(default=None, min_length=2),
):
    obj = await try_return(return_coro=secret.delete(passphrase, id=secret_key))
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passphrase is missing or incorrect",
        )
    return {"status": "secret_deleted"}
