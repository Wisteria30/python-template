from abc import ABC, abstractmethod

from ..entities.meaning import Meaning


class IMeaningRepository(ABC):
    @abstractmethod
    def add(self, entity: Meaning) -> None:
        ...

    @abstractmethod
    def update(self, entity: Meaning) -> None:
        ...

    @abstractmethod
    def save(self, entity: Meaning) -> None:
        ...

    @abstractmethod
    def delete(self, entity: Meaning) -> None:
        ...

    @abstractmethod
    def find_by_id(self, entity_id: int) -> Meaning | None:
        ...

    @abstractmethod
    def find_by_word(self, word: str) -> Meaning | None:
        ...

    @abstractmethod
    def find_by_entity_id(self, entity_id: int) -> Meaning | None:
        ...

    @abstractmethod
    def find_all(self) -> list[Meaning]:
        ...

    @abstractmethod
    def search(self, query: str) -> list[Meaning]:
        ...

    def __getitem__(self, key: int) -> Meaning | None:
        return self.find_by_id(key)
