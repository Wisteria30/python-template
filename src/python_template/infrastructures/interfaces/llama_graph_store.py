from python_template.domains.interfaces import GraphStore
from llama_index.graph_stores import SimpleGraphStore


class LlamaGraphStore(GraphStore):
    def __init__(self, persist_dir: str = "") -> None:
        if persist_dir:
            self._graph_store = SimpleGraphStore().from_persist_dir(persist_dir)
        self._graph_store = SimpleGraphStore()

    def get_client(self) -> object:
        return self._graph_store
