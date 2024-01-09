import weaviate

from python_template.domains.interfaces import VectorStore
from llama_index.vector_stores import WeaviateVectorStore


class LlamaWeaviate(VectorStore):
    def __init__(
        self,
        weaviate_url: str,
    ) -> None:
        # TODO: Authentication
        client = weaviate.Client(weaviate_url)
        self._vector_store = WeaviateVectorStore(weaviate_client=client)

    def get_client(self) -> object:
        return self._vector_store
