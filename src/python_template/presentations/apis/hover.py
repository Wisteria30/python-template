import logging

from python_template.config.container import Container
from python_template.domains.entities import EditorDocument, HoverInput, Position
from python_template.domains.usecases import IHoverUseCase
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from .. import schemas
from ..middleware.logging_context_route import LoggingContextRoute

logger = logging.getLogger(__name__)
router = APIRouter(route_class=LoggingContextRoute)


@router.post("/hover")
@inject
def hover(
    input_data: schemas.HoverInput,
    hover_usecase: IHoverUseCase = Depends(Provide[Container.hover_usecase]),
):
    try:
        position = Position(
            line=input_data.current_doc.position.line,
            character=input_data.current_doc.position.character,
        )
        hover_info = hover_usecase.execute(
            HoverInput(
                repo_name=input_data.repo_name,
                current_doc=EditorDocument(
                    name=input_data.current_doc.name,
                    content=input_data.current_doc.content,
                    position=position,
                ),
            )
        )
    except Exception as e:
        logger.exception(e)
        return schemas.HoverOutput(success=False)

    hover_info = schemas.HoverInfo(
        text=hover_info.text,
        range=schemas.Range(
            start=schemas.Position(
                line=hover_info.range.start.line,
                character=hover_info.range.start.character,
            ),
            end=schemas.Position(
                line=hover_info.range.end.line,
                character=hover_info.range.end.character,
            ),
        ),
    )
    return schemas.HoverOutput(success=True, info=hover_info)
