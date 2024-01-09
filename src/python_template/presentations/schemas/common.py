from pydantic import BaseModel


class Position(BaseModel):
    line: int
    character: int


class Range(BaseModel):
    start: Position
    end: Position


class CurrentDocument(BaseModel):
    name: str
    content: str
    position: Position


class Document(BaseModel):
    name: str
    content: str


class Completion(BaseModel):
    text: str
    range: Range | None
