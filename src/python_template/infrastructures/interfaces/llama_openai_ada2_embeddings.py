import openai

from python_template.domains.interfaces import Embeddings
from llama_index.embeddings import OpenAIEmbedding


class LlamaOpenAIAda2Embeddings(Embeddings):
    def __init__(
        self,
        api_key: str,
    ) -> None:
        openai.api_key = api_key
        self._model = OpenAIEmbedding()

    def get_model(self) -> object:
        return self._model
