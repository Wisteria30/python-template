import logging
import time

from python_template.domains.entities import Document
from python_template.domains.interfaces import Embeddings, GraphStore, IDocumentDataMapper, Llm
from python_template.domains.usecases import IKnowledgeGraphUseCase
from llama_index import KnowledgeGraphIndex, PromptHelper, ServiceContext, StorageContext

# from llama_index.indices.loading import load_index_from_storage
from tqdm import tqdm

logger = logging.getLogger(__name__)


class LlamaKnowledgeGraphUseCase(IKnowledgeGraphUseCase):
    def __init__(
        self,
        llm: Llm,
        embeddings: Embeddings,
        graph_store: GraphStore,
        document_data_mapper: IDocumentDataMapper,
        is_hybrid_search: bool = True,
        sparse_top_k: int = 10,
        persist_dir: str = "",
    ) -> None:
        logger.info("hoge")
        self._llm = llm.get_model()
        self._embed_model = embeddings.get_model()
        self._graph_store = graph_store.get_client()
        self._document_data_mapper = document_data_mapper
        self._is_hybrid_search = is_hybrid_search
        self._sparse_top_k = sparse_top_k
        self._persist_dir = persist_dir
        self._service_context = ServiceContext.from_defaults(
            llm=self._llm,
            embed_model=self._embed_model,
            prompt_helper=PromptHelper(
                num_output=512,
                chunk_size_limit=2000,
                chunk_overlap_ratio=0.2,
                separator="。",
            ),
        )
        self._storage_context = StorageContext.from_defaults(graph_store=self._graph_store)
        self._index = KnowledgeGraphIndex.from_documents(
            [],
            max_triplets_per_chunk=10,
            service_context=self._service_context,
            storage_context=self._storage_context,
            include_embeddings=self._is_hybrid_search,
            show_progress=True,
        )

        self._query_engine = self._index.as_query_engine(
            include_text=False,
            response_mode="tree_summarize",
            embedding_mode="hybrid" if self._is_hybrid_search else "dense",
            similarity_top_k=5,
        )

    def execute(self, query: str) -> str:
        logger.info("searching for query: %s", query)
        prompt = f"「{query}」について日本語で説明してください。"
        results = self._query_engine.query(prompt).response
        return results

    def index_documents(self, documents: list[Document]) -> None:
        llama_documents = [self._document_data_mapper.entity_to_model(doc) for doc in documents]
        for doc in tqdm(llama_documents):
            time.sleep(0.1)
            self._index.insert(doc, show_progress=True)

        if self._persist_dir:
            self._index.storage_context.presist(self._persist_dir)
