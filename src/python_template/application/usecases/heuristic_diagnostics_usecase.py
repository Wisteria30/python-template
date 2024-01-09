import logging

from python_template.domains.entities import (
    Diagnostics,
    DiagnosticsInput,
)
from python_template.domains.interfaces import INlpClient
from python_template.domains.usecases import IDiagnosticUseCase

logger = logging.getLogger(__name__)


class HeuristicDiagnosticUseCase(IDiagnosticUseCase):
    def __init__(
        self,
        nlp_client: INlpClient,
    ) -> None:
        self._nlp_client = nlp_client

    async def execute(self, input_: DiagnosticsInput) -> Diagnostics:
        doc = input_.current_doc.content
        try:
            diagnostics = self._nlp_client.proofread(doc)
            return diagnostics
        except Exception as e:
            raise e
