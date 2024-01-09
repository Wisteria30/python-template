from abc import ABC, abstractmethod

from ..entities.documents import Document


class IDocumentRepository(ABC):
    """An interface for a repository of Document entity."""

    @abstractmethod
    def add(self, entity: Document) -> None:
        ...

    @abstractmethod
    def update(self, entity: Document) -> None:
        ...

    @abstractmethod
    def save(self, entity: Document) -> None:
        ...

    @abstractmethod
    def delete(self, entity: Document) -> None:
        ...

    @abstractmethod
    def find_by_id(self, entity_id: int) -> Document | None:
        ...

    @abstractmethod
    def find_all(self) -> list[Document]:
        raise NotImplementedError

    def __getitem__(self, key: int) -> Document | None:
        return self.find_by_id(key)
