import logging
import pickle

from python_template.domains.entities import Document
from python_template.domains.interfaces import IDocumentRepository

logger = logging.getLogger(__name__)


class FileDocumentRepository(IDocumentRepository):
    def __init__(self, path: str) -> None:
        self.path = path
        self.documents: list[Document] = []
        try:
            with open(self.path, "rb") as f:
                self.documents = pickle.load(f)
        except FileNotFoundError as e:
            logger.warning(e)

    def add(self, entity: Document) -> None:
        self.documents.append(entity)
        self._dump()

    def update(self, entity: Document) -> None:
        for i, doc in enumerate(self.documents):
            if doc.id == entity.id:
                self.documents[i] = entity
        self._dump()

    def save(self, entity: Document) -> None:
        for i, doc in enumerate(self.documents):
            if doc.id == entity.id:
                self.documents[i] = entity
                self._dump()
                return
        self.add(entity)

    def delete(self, entity: Document) -> None:
        for i, doc in enumerate(self.documents):
            if doc.id == entity.id:
                del self.documents[i]
        self._dump()

    def find_by_id(self, entity_id: int) -> Document | None:
        for doc in self.documents:
            if doc.id == entity_id:
                return doc
        return None

    def find_all(self) -> list[Document]:
        return self.documents

    def __getitem__(self, key: int) -> Document | None:
        return self.find_by_id(key)

    def _dump(self) -> None:
        with open(self.path, "wb") as f:
            pickle.dump(self.documents, f)
