import logging
import sys

from python_template.config.container import Container
from python_template.domains.usecases import IDocumentPreprocessingUseCase
from dependency_injector.wiring import Provide, inject
from fire import Fire

logger = logging.getLogger(__name__)


@inject
def run_preprocess(
    path: str,
    directory_preprocessing_usecase: IDocumentPreprocessingUseCase = Provide[
        Container.directory_preprocessing_usecase
    ],
    do_save: bool = True,
    do_index: bool = True,
    do_entity: bool = True,
    do_dict: bool = True,
) -> None:
    """Run indexer"""
    logger.info("run preprocessor")
    try:
        directory_preprocessing_usecase.execute(
            path=path, do_save=do_save, do_index=do_index, do_entity=do_entity, do_dict=do_dict
        )
    except Exception as e:
        logger.error(e, exc_info=True)
        raise e
    logger.info("finish preprocessor")


def run(
    path: str = "data/pksha_note/",
    do_save: bool = True,
    do_index: bool = True,
    do_entity: bool = True,
    do_dict: bool = True,
) -> None:
    container = Container()
    container.wire(modules=[sys.modules[__name__]])
    run_preprocess(path, do_save=do_save, do_index=do_index, do_entity=do_entity, do_dict=do_dict)


if __name__ == "__main__":
    Fire(run)
