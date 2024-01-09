from python_template.domains.interfaces import GraphStore
from llama_index.graph_stores import Neo4jGraphStore


class LlamaNeo4j(GraphStore):
    def __init__(
        self,
        username: str,
        password: str,
        url: str,
        database: str,
    ) -> None:
        self._graph_store = Neo4jGraphStore(
            username=username,
            password=password,
            url=url,
            database=database,
        )

    def get_client(self) -> object:
        return self._graph_store
