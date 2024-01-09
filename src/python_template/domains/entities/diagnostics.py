from typing import Literal

from pydantic import BaseModel

from .positions import EditorDocument, Range


class Diagnostic(BaseModel):
    message: str
    severity: Literal["error", "warn", "info", "hint"]
    range: Range


class Diagnostics(BaseModel):
    diagnostics: list[Diagnostic]


class DiagnosticsInput(BaseModel):
    instruction: str
    repo_name: str
    current_doc: EditorDocument
    relevant_docs: list[EditorDocument]


class DiagnosticsOutput(BaseModel):
    success: bool
    diagnostics: list[Diagnostic]
