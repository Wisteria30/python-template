from python_template.domains.interfaces import VectorStore
from llama_index.vector_stores import PGVectorStore
from sqlalchemy.engine.url import make_url


class LlamaPGVector(VectorStore):
    def __init__(
        self,
        postgres_connection_string: str,
        table_name: str,
        embed_dim: int,
        is_hybrid_search: bool = True,
        text_search_config: str = "japanese",
    ) -> None:
        url = make_url(postgres_connection_string)
        self._vector_store = PGVectorStore.from_params(
            host=url.host,
            port=url.port,
            user=url.username,
            password=url.password,
            database=url.database,
            table_name=table_name,
            embed_dim=embed_dim,
            hybrid_search=is_hybrid_search,
            text_search_config=text_search_config,
        )

    def get_client(self) -> object:
        return self._vector_store
