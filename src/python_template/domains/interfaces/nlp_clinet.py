from abc import ABC, abstractmethod

from ..entities.diagnostics import Diagnostics
from ..entities.nlp_entities import NlpEntity
from ..entities.positions import Position, Range


class INlpClient(ABC):
    @abstractmethod
    def extract_entities(self, text: str) -> list[NlpEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_morpheme_by_position(self, text: str, position: Position) -> tuple[str, Range]:
        raise NotImplementedError

    @abstractmethod
    def proofread(self, text: str) -> Diagnostics:
        """文章を校正する"""
        raise NotImplementedError
