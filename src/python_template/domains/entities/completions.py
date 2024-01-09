from pydantic import BaseModel

from .positions import Range


class Completion(BaseModel):
    text: str
    range: Range | None

    @staticmethod
    def create(text: str, range: Range | None = None) -> "Completion":
        return Completion(text=text, range=range)
