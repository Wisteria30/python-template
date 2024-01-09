from abc import ABC, abstractmethod


class INlpEntityUseCase(ABC):
    @abstractmethod
    def execute(self, text: str) -> None:
        raise NotImplementedError
