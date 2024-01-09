from pydantic import BaseModel


class Meaning(BaseModel):
    """言葉の意味を表すドメインモデル"""

    id: int | None
    word: str
    meaning: str
    entity_id: int | None

    @classmethod
    def create(cls, word: str, meaning: str, entity_id: int | None = None) -> "Meaning":
        return Meaning(id=None, word=word, meaning=meaning, entity_id=entity_id)
