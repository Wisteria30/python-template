import logging

from python_template.config.container import Container
from python_template.domains.entities import DiagnosticsInput, EditorDocument
from python_template.domains.usecases import IDiagnosticUseCase
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from .. import schemas
from ..middleware.logging_context_route import LoggingContextRoute

logger = logging.getLogger(__name__)
router = APIRouter(route_class=LoggingContextRoute)


@router.post("/diagnostics")
@inject
async def diagnostics(
    input_data: schemas.DiagnosticsInput,
    fast: bool = False,
    heuristic_diagnostics_usecase: IDiagnosticUseCase = Depends(
        Provide[Container.heuristic_diagnostics_usecase]
    ),
    diagnostics_usecase: IDiagnosticUseCase = Depends(Provide[Container.diagnostics_usecase]),
) -> schemas.DiagnosticsOutput:
    input_ = DiagnosticsInput(
        repo_name=input_data.repo_name,
        instruction=input_data.instruction,
        current_doc=EditorDocument(
            content=input_data.current_doc.content,
            name=input_data.current_doc.name,
        ),
        relevant_docs=[
            EditorDocument(
                content=doc.content,
                name=doc.name,
            )
            for doc in input_data.relevant_docs
        ],
    )

    try:
        if fast:
            result = await heuristic_diagnostics_usecase.execute(input_)
        else:
            result = await diagnostics_usecase.execute(input_)
    except Exception as e:
        logging.error(e)
        return schemas.DiagnosticsOutput(
            success=False,
            diagnostics=[
                schemas.Diagnostic(
                    message="Unexpected error",
                    severity="error",
                    range=schemas.Range(
                        start=schemas.Position(
                            line=0,
                            character=0,
                        ),
                        end=schemas.Position(
                            line=0,
                            character=1,
                        ),
                    ),
                )
            ],
        )

    diagnostics = [
        schemas.Diagnostic(
            message=diagnostic.message,
            severity=diagnostic.severity,
            range=schemas.Range(
                start=schemas.Position(
                    line=diagnostic.range.start.line,
                    character=diagnostic.range.start.character,
                ),
                end=schemas.Position(
                    line=diagnostic.range.end.line,
                    character=diagnostic.range.end.character,
                ),
            ),
        )
        for diagnostic in result.diagnostics
    ]

    return schemas.DiagnosticsOutput(
        success=True,
        diagnostics=diagnostics,
    )
