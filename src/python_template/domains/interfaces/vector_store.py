from abc import ABC, abstractmethod


class VectorStore(ABC):
    """
    一旦外部ライブラブのdb clientを直接返すWrapperにする
    """

    @abstractmethod
    def get_client(self) -> object:
        raise NotImplementedError
