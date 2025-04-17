"""Application concrete dependencies."""

from typing import Annotated

from fastapi import Depends
from src.services.secret import SecretService

secret_service = Annotated[SecretService, Depends()]
