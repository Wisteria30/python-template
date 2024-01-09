import logging

from python_template.domains.interfaces import IPageReader
from python_template.domains.usecases import (
    IDocumentPreprocessingUseCase,
    IKnowledgeGraphUseCase,
    INlpEntityUseCase,
    IRagUseCase,
)

logger = logging.getLogger(__name__)


class NotionPreprocessingUseCase(IDocumentPreprocessingUseCase):
    def __init__(
        self,
        page_reader: IPageReader,
        nlp_entity_usecase: INlpEntityUseCase,
        rag_usecase: IRagUseCase,
        knowledge_graph_usecase: IKnowledgeGraphUseCase,
    ) -> None:
        self.page_reader = page_reader
        self.nlp_entity_usecase = nlp_entity_usecase
        self.rag_usecase = rag_usecase
        self.knowledge_graph_usecase = knowledge_graph_usecase

    def execute(self) -> None:
        documents = self.page_reader.load()
        self.rag_usecase.index_documents(documents)
        self.knowledge_graph_usecase.index_documents(documents)
        # エンティティ登録も同時に行う
        for document in documents:
            self.nlp_entity_usecase.execute(document.text)
