from python_template.domains.interfaces import Llm
from llama_index.llms import OpenAI
from llama_index.prompts import ChatMessage, MessageRole


class LlamaGpt35Turbo(Llm):
    def __init__(
        self,
        api_key: str,
    ) -> None:
        self._model = OpenAI(
            model="gpt-3.5-turbo",
            api_key=api_key,
            temperature=0,
        )

    def get_model(self) -> object:
        return self._model

    def complete(self, _text: str, instruction: str = "") -> str:
        if instruction == "":
            return self._model.complete(_text).text
        else:
            chat_message = [
                ChatMessage(
                    role=MessageRole.SYSTEM,
                    content=instruction,
                ),
                ChatMessage(
                    role=MessageRole.USER,
                    content=_text,
                ),
            ]
            return self._model.chat(chat_message).message.content
