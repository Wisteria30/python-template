from abc import ABC, abstractmethod

from ..entities.completions import Completion


class ICompletionUseCase(ABC):
    @abstractmethod
    def execute(self, query: str) -> list[Completion]:
        raise NotImplementedError
