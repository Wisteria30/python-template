from abc import ABC, abstractmethod


class IKnowledgeGraphUseCase(ABC):
    @abstractmethod
    def execute(self, query: str) -> str:
        raise NotImplementedError
