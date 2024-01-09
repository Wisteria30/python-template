from typing import Protocol

from fastapi import APIRouter


class APIProtocol(Protocol):
    router: APIRouter


__all__ = ["APIProtocol"]
