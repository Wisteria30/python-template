import bisect
import logging

import spacy


# from fugashi import Tagger
from python_template.domains.entities import NlpEntity, Position, Range
from python_template.domains.interfaces import INlpClient

logger = logging.getLogger(__name__)


class GinzaNlpClient(INlpClient):
    def __init__(self) -> None:
        self.nlp = spacy.load("ja_ginza")
        # self.tagger = Tagger("-Owakati")

    def extract_entities(self, text: str) -> list[NlpEntity]:
        doc = self.nlp(text)
        entities = {}
        # wordが一致したらfrequencyを+1する
        for ent in doc.ents:
            if ent.text in entities:
                entities[ent.text].frequency += 1
            else:
                entity = NlpEntity.create(ent.text, ent.label_, 1)
                entities[ent.text] = entity

        entities: list[NlpEntity] = list(entities.values())
        return entities

    def get_morpheme_by_position(self, text: str, position: Position) -> tuple[str, Range]:
        """形態素解析の結果から、指定した位置の形態素を返す
        1. positionとtextから、文字列のindexを計算する
        2. textの形態素解析を行い、positionのindexに対応する形態素を返す
        """
        index: int = position.get_index(text)
        doc = self.nlp(text)

        # docの末尾が改行・空文字なら削除
        if doc[-1].text in ["\n", ""]:
            doc = doc[:-1]

        # 二分探索でindexに対応する形態素を探す
        doc_idxs = [token.idx for token in doc]
        idx = bisect.bisect_right(doc_idxs, index) - 1

        if idx < 0 or idx >= len(doc):
            logger.warning(
                "index out of range", extra={"index": idx, "text": text, "position": position}
            )
            return "", None

        # 形態素の範囲を計算
        range_ = Range(
            start=Position.create_from_index(text, doc[idx].idx),
            end=Position.create_from_index(text, doc[idx].idx + len(doc[idx].text)),
        )

        return doc[idx].text, range_

    def proofread(self, text: str) -> list[tuple[str, Range]]:
        """文章を校正する"""
        raise NotImplementedError
