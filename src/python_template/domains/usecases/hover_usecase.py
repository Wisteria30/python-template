from abc import ABC, abstractmethod

from ..entities.hover import HoverInfo, HoverInput


class IHoverUseCase(ABC):
    @abstractmethod
    def execute(self, input_data: HoverInput) -> HoverInfo:
        raise NotImplementedError
