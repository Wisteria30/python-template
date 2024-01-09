from abc import ABC, abstractmethod
from typing import Any

from ..entities.documents import Document


class IRagUseCase(ABC):
    @abstractmethod
    def execute(self, query: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def index_documents(self, documents: list[Document]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_index(self) -> Any:
        # TODO: VectorStoreIndex Interfaceをdomainで定義する
        raise NotImplementedError
