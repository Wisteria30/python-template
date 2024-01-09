from python_template.domains.entities.documents import Document
from python_template.domains.interfaces import IDocumentDataMapper, IPageReader
from llama_index import NotionPageReader


class LlamaNotionPageReader(IPageReader):
    def __init__(
        self, notion_integration_token: str, document_data_mapper: IDocumentDataMapper
    ) -> None:
        self.reader = NotionPageReader(integration_token=notion_integration_token)
        self.data_mapper = document_data_mapper

    def load(self, path: str = "") -> list[Document]:
        try:
            page_ids = self.reader.search(path)
            response = self.reader.load_data(page_ids)
        except Exception as e:
            raise e

        documents = [self.data_mapper.model_to_entity(instance) for instance in response]
        return documents
