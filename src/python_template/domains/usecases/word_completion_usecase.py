from abc import ABC, abstractmethod

from ..entities.completions import Completion
from ..entities.positions import Position


class IWordCompletionUseCase(ABC):
    @abstractmethod
    def execute(self, content: str, position: Position) -> list[Completion]:
        raise NotImplementedError
