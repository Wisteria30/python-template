from abc import ABC, abstractmethod


class Llm(ABC):
    """
    一旦外部のllmライブラリを直接返すWrapperにする
    """

    @abstractmethod
    def get_model(self) -> object:
        raise NotImplementedError

    @abstractmethod
    def complete(self, _text: str, instruction: str = "") -> str:
        raise NotImplementedError
