import logging

from python_template.config.container import Container
from python_template.domains.entities import Position, Range
from python_template.domains.usecases import ICompletionUseCase
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from ..middleware.logging_context_route import LoggingContextRoute
from ..schemas import Completion, CompletionInput, CompletionOutput

logger = logging.getLogger(__name__)
router = APIRouter(route_class=LoggingContextRoute)


@router.post("/completions")
@inject
def completion(
    input_data: CompletionInput,
    completion_usecase: ICompletionUseCase = Depends(Provide[Container.completion_usecase]),
) -> CompletionOutput:
    try:
        start_position = Position(
            line=input_data.current_doc.position.line,
            character=input_data.current_doc.position.character,
        )
        end_position = Position(
            line=input_data.current_doc.position.line,
            character=input_data.current_doc.position.character + 6,
        )
        range = Range(start=start_position, end=end_position)
        completions = completion_usecase.execute(input_data.current_doc.content)
        completions_string = [
            Completion(
                text=completion.text,
                range=range,
            )
            for completion in completions
        ]
    except Exception as e:
        logger.error(f"completion error: {e}")
        return CompletionOutput(
            success=False,
            completions=[],
        )
    return CompletionOutput(
        success=True,
        completions=completions_string,
    )
