import logging

from python_template.config.container import Container
from python_template.domains.entities import Position
from python_template.domains.usecases import IWordCompletionUseCase
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from ..middleware.logging_context_route import LoggingContextRoute
from ..schemas import WordCompletionInput, WordCompletionOutput

logger = logging.getLogger(__name__)
router = APIRouter(route_class=LoggingContextRoute)


@router.post("/word-completions")
@inject
def word_completion(
    input_data: WordCompletionInput,
    word_completion_usecase: IWordCompletionUseCase = Depends(
        Provide[Container.word_completion_usecase]
    ),
):
    try:
        position = Position(
            line=input_data.current_doc.position.line,
            character=input_data.current_doc.position.character,
        )
        completions = word_completion_usecase.execute(
            content=input_data.current_doc.content, position=position
        )
    except Exception as e:
        logger.exception(e)
        return WordCompletionOutput(success=False, completions=[])

    logger.info(f"completions: {completions}")
    return WordCompletionOutput(success=True, completions=completions)
