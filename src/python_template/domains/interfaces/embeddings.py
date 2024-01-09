from abc import ABC, abstractmethod


class Embeddings(ABC):
    @abstractmethod
    def get_model(self) -> object:
        raise NotImplementedError
