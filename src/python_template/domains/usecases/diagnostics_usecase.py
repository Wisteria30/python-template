from abc import ABC, abstractmethod

from ..entities.diagnostics import Diagnostics, DiagnosticsInput


class IDiagnosticUseCase(ABC):
    @abstractmethod
    async def execute(self, input: DiagnosticsInput) -> Diagnostics:
        raise NotImplementedError
