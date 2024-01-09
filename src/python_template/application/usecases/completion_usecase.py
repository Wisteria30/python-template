import logging

from python_template.domains.entities.completions import Completion
from python_template.domains.interfaces import Llm
from python_template.domains.usecases import ICompletionUseCase

logger = logging.getLogger(__name__)


class CompletionUseCase(ICompletionUseCase):
    def __init__(self, llm: Llm) -> None:
        self.llm = llm

    def execute(self, query: str) -> list[Completion]:
        query = query.strip()
        if query == "":
            return [Completion.create("")]

        instruction = """
        You are a first-class businessman. Please write a continuation of the sentence you are currently writing in 日本語.
        - Please write in a way that does not duplicate sentences and leads to the next story.
        - Do not generate what has already been written in the query.
        - Limit it to 2 or 3 sentences."""

        answer = self.llm.complete(query, instruction=instruction)
        # rag_stringの先頭がqueryと重複する場合は削除する
        while answer.startswith(query):
            answer = answer[len(query) :]
        # 「。」がある場合は改行する
        answer = answer.replace("。", "。\n")

        completions = [Completion.create(answer)]
        return completions
