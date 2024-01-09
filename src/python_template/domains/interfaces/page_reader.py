from abc import ABC, abstractmethod

from ..entities.documents import Document


class IPageReader(ABC):
    @abstractmethod
    def load(self, path: str = "") -> list[Document]:
        raise NotImplementedError
