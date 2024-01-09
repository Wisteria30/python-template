import logging
import sys

from python_template.config.container import Container
from python_template.domains.usecases import IDocumentPreprocessingUseCase
from dependency_injector.wiring import Provide, inject

logger = logging.getLogger(__name__)


@inject
def run_indexer(
    notion_preprocessing_usecase: IDocumentPreprocessingUseCase = Provide[
        Container.notion_preprocessing_usecase
    ],
) -> None:
    """Run indexer"""
    logger.info("run indexer")
    try:
        notion_preprocessing_usecase.execute()
    except Exception as e:
        logger.error(e, exc_info=True)
        raise e
    logger.info("finish indexer")


def run() -> None:
    container = Container()
    container.wire(modules=[sys.modules[__name__]])
    run_indexer()
