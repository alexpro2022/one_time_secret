from fastapi import APIRouter, status
from src.config.app_config import app_conf
from src.api.endpoints.utils import try_return
from src.api.responses import response_404
from src.api.schemas import secret as schemas
from src.repo.models import Secret as repo_model
from src.services import secret
from src.types_app import TypePK, async_session

router = APIRouter(prefix=f"{app_conf.URL_PREFIX}/secret", tags=["Secrets"])


@router.post(
    "",
    summary="create secret",
    description=secret.create.__doc__,
    status_code=status.HTTP_201_CREATED,
    # response_model=schemas.SecretKey,
)
async def create_secret(session: async_session, create_secret: schemas.SecretCreate):
    return await secret.create(
        session=session,
        model=repo_model,
        **create_secret.model_dump(),
    )


@router.get(
    "/{secret_key}",
    summary="get secret",
    description=secret.get.__doc__,
    # response_model=schemas.Secret,
    responses=response_404("secret"),
)
async def get_secret(session: async_session, secret_key: TypePK):
    return await try_return(
        return_coro=secret.get(
            session=session,
            model=repo_model,
            id=secret_key,
        )
    )


@router.delete(
    "/{secret_key}",
    summary="delete secret",
    description=secret.delete.__doc__,
    # response_model=schemas.SecretDelete,
    responses=response_404("secret"),
)
async def delete_secret(session: async_session, secret_key: TypePK):
    return await try_return(
        return_coro=secret.delete(
            session=session,
            model=repo_model,
            id=secret_key,
        )
    )
