import logging

from python_template.domains.interfaces import IDocumentRepository
from python_template.domains.usecases import (
    IDictionaryUseCase,
    IDocumentPreprocessingUseCase,
    INlpEntityUseCase,
    IRagUseCase,
)

logger = logging.getLogger(__name__)


class DocumentPreprocessingUseCase(IDocumentPreprocessingUseCase):
    def __init__(
        self,
        document_repository: IDocumentRepository,
        dictionary_usecase: IDictionaryUseCase,
        nlp_entity_usecase: INlpEntityUseCase,
        rag_usecase: IRagUseCase,
    ) -> None:
        self.document_repository = document_repository
        self.dictionary_usecase = dictionary_usecase
        self.nlp_entity_usecase = nlp_entity_usecase
        self.rag_usecase = rag_usecase

    def execute(
        self, do_index: bool = False, do_entity: bool = True, do_dict: bool = False
    ) -> None:
        logger.info("run preprocessor")
        documents = self.document_repository.find_all()

        if do_index:
            logger.info("index documents")
            self.rag_usecase.index_documents(documents)

        if do_entity:
            logger.info("extract entities")
            MAX_LENGTH = 10000
            for document in documents:
                for i in range(0, len(document.text), MAX_LENGTH):
                    text = document.text[i : i + MAX_LENGTH]
                    self.nlp_entity_usecase.execute(text)

        if do_dict:
            logger.info("construct dictionary")
            self.dictionary_usecase.execute()
