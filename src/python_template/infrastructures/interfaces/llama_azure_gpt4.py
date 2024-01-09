from python_template.domains.interfaces import Llm
from llama_index.llms import AzureOpenAI


class LlamaAzureGpt4(Llm):
    def __init__(
        self,
        engine: str,
        endpoint_url: str,
        api_key: str,
        api_version: str,
    ) -> None:
        self._model = AzureOpenAI(
            engine=engine,
            model="gpt-4",
            temperature=0,
            api_base=endpoint_url,
            api_key=api_key,
            api_type="azure",
            api_version=api_version,
        )

    def get_model(self) -> object:
        return self._model

    def complete(self, _text: str) -> str:
        return self._model.complete(_text).text
