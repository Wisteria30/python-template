from abc import ABC, abstractmethod


class IDictionaryUseCase(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError
