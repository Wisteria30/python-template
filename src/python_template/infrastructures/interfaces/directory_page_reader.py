import logging

from python_template.domains.entities import Document
from python_template.domains.interfaces import IDocumentDataMapper, IPageReader
from llama_index import SimpleDirectoryReader

logger = logging.getLogger(__name__)


class DirectoryPageReader(IPageReader):
    def __init__(
        self,
        document_data_mapper: IDocumentDataMapper,
    ) -> None:
        self.data_mapper = document_data_mapper

    def load(self, path: str) -> list[Document]:
        logger.info(f"load documents from {path}")
        reader = SimpleDirectoryReader(
            input_dir=path,
            recursive=True,
            file_metadata=lambda x: {"title": x.split("/")[-1]},
        )
        docs = reader.load_data()

        logger.info(f"loaded {len(docs)} documents")

        documents = [self.data_mapper.model_to_entity(instance) for instance in docs]
        return documents
