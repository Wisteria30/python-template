from pydantic import BaseModel


class Position(BaseModel):
    line: int
    character: int

    def get_index(self, text: str) -> int:
        """指定された行と文字から、文字列内のインデックスを計算する"""
        index = 0
        _line = 0
        _character = 0
        for c in text:
            if _line == self.line and _character == self.character:
                break
            if c == "\n":
                _line += 1
                _character = 0
            else:
                _character += 1
            index += 1
        return index

    @staticmethod
    def create_from_index(text: str, index: int) -> "Position":
        """指定されたインデックスから、Positionを生成する"""
        line = 0
        character = 0

        for i, c in enumerate(text):
            if i == index:
                break
            if c == "\n":
                line += 1
                character = 0
            else:
                character += 1

        return Position(line=line, character=character)


class Range(BaseModel):
    start: Position
    end: Position


class EditorDocument(BaseModel):
    name: str
    content: str
    position: Position | None
