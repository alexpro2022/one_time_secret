from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status

from src.api.endpoints.utils import set_headers_no_client_cache, try_return
from src.api.responses import response_400, response_404
from src.api.schemas import secret as schemas
from src.config.app_config import app_conf
from src.services import secret
from src.types_app import ClientInfo, TypePK, async_session

router = APIRouter(
    prefix=f"{app_conf.url_prefix}/secret",
    tags=["Secrets"],
    dependencies=[Depends(set_headers_no_client_cache)],
)


@router.post(
    "",
    summary="create secret",
    description=secret.create.__doc__,
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.SecretKey,
)
async def create_secret(
    client_info: ClientInfo,
    session: async_session,
    bg_tasks: BackgroundTasks,
    create_secret: schemas.SecretCreate,
):
    obj = await secret.create(
        client_info, session, bg_tasks, **create_secret.model_dump()
    )
    return {"secret_key": str(obj.id)}


@router.get(
    "/{secret_key}",
    summary="get secret",
    description=secret.get.__doc__,
    response_model=schemas.Secret,
    responses=response_404("secret"),
)
async def get_secret(
    client_info: ClientInfo,
    session: async_session,
    bg_tasks: BackgroundTasks,
    secret_key: TypePK,
):
    obj = await try_return(
        return_coro=secret.get(client_info, session, bg_tasks, id=secret_key)
    )
    return {"secret": obj.secret}


@router.delete(
    "/{secret_key}",
    summary="delete secret",
    description=secret.delete.__doc__,
    response_model=schemas.SecretDelete,
    responses={
        **response_400("Passphrase is missing or incorrect"),
        **response_404("secret"),
    },
)
async def delete_secret(
    client_info: ClientInfo,
    session: async_session,
    bg_tasks: BackgroundTasks,
    secret_key: TypePK,
    passphrase: str | None = Query(default=None, min_length=2),
):
    obj = await try_return(
        return_coro=secret.delete(
            client_info, session, bg_tasks, passphrase, id=secret_key
        )
    )
    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passphrase is missing or incorrect",
        )
    return {"status": "secret_deleted"}
