from abc import ABC, abstractmethod
from typing import Any

from ..entities.documents import Document


class IDocumentDataMapper(ABC):
    @abstractmethod
    def entity_to_model(self, document: Document) -> Any:
        pass

    @abstractmethod
    def model_to_entity(self, document: Any) -> Document:
        pass
