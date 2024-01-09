from typing import Any

from pydantic import BaseModel


class Document(BaseModel):
    """LlamaIndexのDocument構造をドメインモデルとして暫定定義"""

    id: str
    embedding: list[float] | None
    metadata: dict[str, Any]
    excluded_embed_metadata_keys: list[str]
    excluded_llm_metadata_keys: list[str]
    relationships: dict[str, Any]
    hash: str
    text: str
    start_char_idx: int | None
    end_char_idx: int | None
    text_template: str
    metadata_template: str
    metadata_seperator: str
    class_name: str
