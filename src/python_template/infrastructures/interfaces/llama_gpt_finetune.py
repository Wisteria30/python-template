from python_template.domains.interfaces import Llm
from llama_index.llms import OpenAI
from llama_index.prompts import ChatMessage, MessageRole


class LlamaGptFineTune(Llm):
    def __init__(
        self,
        model: str,
        api_key: str,
    ) -> None:
        try:
            self._model = OpenAI(
                model=model,
                api_key=api_key,
                temperature=0,
            )
        except Exception as e:
            raise ValueError(f"OpenAI model '{model}' is not found") from e

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
