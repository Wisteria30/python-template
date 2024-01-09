from abc import ABC, abstractmethod


class IDocumentPreprocessingUseCase(ABC):
    @abstractmethod
    def execute(self, data: dict) -> None:
        raise NotImplementedError
