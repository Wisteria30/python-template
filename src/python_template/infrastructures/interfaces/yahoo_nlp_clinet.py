import json
import logging

from typing import Any
from urllib import request

from python_template.domains.entities import Diagnostic, Diagnostics, NlpEntity, Position, Range
from python_template.domains.interfaces import INlpClient

logger = logging.getLogger(__name__)

rule_severity_map = {
    # 1. 表記・表現の間違いや不適切な表現に関する指摘
    "誤変換": "warn",
    "誤用": "warn",
    "使用注意": "warn",
    "不快語": "warn",
    "機種依存または拡張文字": "warn",
    "外国地名": "warn",
    "固有名詞": "warn",
    "人名": "warn",
    "ら抜き": "warn",
    # 2. わかりやすい表記にするための指摘
    "当て字": "info",
    "表外漢字あり": "info",
    "用字": "info",
    # 3. 文章をよりよくするための指摘
    "用語言い換え（商標など）": "hint",
    "二重否定": "hint",
    "助詞不足の可能性あり": "hint",
    "冗長表現": "hint",
    "略語": "hint",
}


class YahooNlpClient(INlpClient):
    def __init__(self, client_id: str) -> None:
        self.client_id = client_id

    def extract_entities(self, text: str) -> list[NlpEntity]:
        raise NotImplementedError

    def get_morpheme_by_position(self, text: str, position: Position) -> tuple[str, Range]:
        raise NotImplementedError

    def proofread(self, text: str) -> Diagnostics:
        """文章を校正する"""

        def _build_correct(word: str, suggestion: str, rule: str, note: str) -> str:
            """ex:
            助詞不足の可能性あり: 高度化
            表外漢字あり: 尖  ※尖は表外漢字
            用字: ソフトウェア -> ソフトウエア
            用字: 等 -> など  ※「とう」と読む場合は漢字表記可
            """
            if suggestion == "" and note == "":
                return f"{rule}: {word}"
            elif suggestion == "":
                return f"{rule}: {word}  ※{note}"
            elif note == "":
                return f"{rule}: {word} -> {suggestion}"
            else:
                return f"{rule}: {word} -> {suggestion}  ※{note}"

        url = "https://jlp.yahooapis.jp/KouseiService/V2/kousei"
        method = "jlp.kouseiservice.kousei"
        res = self._post(text, url, method)
        diagnostics = Diagnostics(diagnostics=[])

        for suggest in res["result"]["suggestions"]:
            offset = int(suggest["offset"])
            length = int(suggest["length"])
            diagnostic = Diagnostic(
                message=_build_correct(
                    suggest["word"],
                    suggest["suggestion"],
                    suggest["rule"],
                    suggest["note"],
                ),
                severity=rule_severity_map[suggest["rule"]],
                range=Range(
                    start=Position.create_from_index(text, offset),
                    end=Position.create_from_index(text, offset + length),
                ),
            )
            diagnostics.diagnostics.append(diagnostic)

        return diagnostics

    def _post(self, query: str, url: str, method: str, id_: str = "1234-1") -> Any:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"Yahoo AppID: {self.client_id}",
        }
        param_dic = {
            "id": id_,
            "jsonrpc": "2.0",
            "method": method,
            "params": {"q": query},
        }
        try:
            params = json.dumps(param_dic).encode()
            req = request.Request(url, params, headers)
            with request.urlopen(req) as res:
                body = res.read()
            return json.loads(body.decode("utf-8"))
        except Exception as e:
            logger.error(e)
            raise e
