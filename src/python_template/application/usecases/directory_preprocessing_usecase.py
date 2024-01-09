import logging

from python_template.domains.interfaces import IDocumentRepository, IPageReader
from python_template.domains.usecases import (
    IDictionaryUseCase,
    IDocumentPreprocessingUseCase,
    INlpEntityUseCase,
    IRagUseCase,
)

logger = logging.getLogger(__name__)


class DirectoryPreprocessingUseCase(IDocumentPreprocessingUseCase):
    def __init__(
        self,
        page_reader: IPageReader,
        document_repository: IDocumentRepository,
        dictionary_usecase: IDictionaryUseCase,
        nlp_entity_usecase: INlpEntityUseCase,
        rag_usecase: IRagUseCase,
    ) -> None:
        self.page_reader = page_reader
        self.document_repository = document_repository
        self.dictionary_usecase = dictionary_usecase
        self.nlp_entity_usecase = nlp_entity_usecase
        self.rag_usecase = rag_usecase

    def execute(
        self,
        path: str,
        do_save: bool = True,
        do_index: bool = False,
        do_entity: bool = True,
        do_dict: bool = False,
    ) -> None:
        logger.info("run preprocessor")
        documents = self.page_reader.load(path=path)

        if do_save:
            logger.info("save documents")
            for document in documents:
                self.document_repository.save(document)

        if do_index:
            logger.info("index documents")
            self.rag_usecase.index_documents(documents)

        if do_entity:
            logger.info("extract entities")
            for document in documents:
                self.nlp_entity_usecase.execute(document.text)

        if do_dict:
            logger.info("construct dictionary")
            self.dictionary_usecase.execute()
