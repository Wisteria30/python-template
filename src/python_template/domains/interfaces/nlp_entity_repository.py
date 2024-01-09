from abc import ABC, abstractmethod

from ..entities.nlp_entities import NlpEntity


class INlpEntityRepository(ABC):
    """An interface for a repository of NlpEntity entity."""

    @abstractmethod
    def add(self, entity: NlpEntity) -> None:
        ...

    @abstractmethod
    def update(self, entity: NlpEntity) -> None:
        ...

    @abstractmethod
    def save(self, entity: NlpEntity) -> None:
        ...

    @abstractmethod
    def delete(self, entity: NlpEntity) -> None:
        ...

    @abstractmethod
    def find_by_id(self, entity_id: int) -> NlpEntity | None:
        ...

    @abstractmethod
    def find_by_word(self, word: str) -> NlpEntity | None:
        ...

    @abstractmethod
    def find_all(self) -> list[NlpEntity]:
        ...

    @abstractmethod
    def search(self, query: str) -> list[NlpEntity]:
        ...

    def __getitem__(self, key: int) -> NlpEntity | None:
        return self.find_by_id(key)
