from pydantic import BaseModel

from .positions import EditorDocument, Range


class HoverInfo(BaseModel):
    text: str
    range: Range


class HoverInput(BaseModel):
    repo_name: str
    current_doc: EditorDocument
