from pydantic import BaseModel


class NlpEntity(BaseModel):
    id: int | None
    word: str
    label: str
    frequency: int

    @staticmethod
    def create(word: str, label: str, frequency: int) -> "NlpEntity":
        return NlpEntity(id=None, word=word, label=label, frequency=frequency)
