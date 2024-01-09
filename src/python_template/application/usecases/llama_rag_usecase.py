from typing import Any, Optional

from python_template.domains.entities import Document
from python_template.domains.interfaces import Embeddings, IDocumentDataMapper, Llm, VectorStore
from python_template.domains.usecases import IRagUseCase
from llama_index import ServiceContext, StorageContext, VectorStoreIndex
from llama_index.callbacks import CallbackManager, LlamaDebugHandler, WandbCallbackHandler
from llama_index.callbacks.base_handler import BaseCallbackHandler
from llama_index.callbacks.schema import CBEventType, EventPayload
from tqdm import tqdm


class LlamaRagUseCase(IRagUseCase):
    def __init__(
        self,
        llm: Llm,
        embeddings: Embeddings,
        vector_store: VectorStore,
        document_data_mapper: IDocumentDataMapper,
        chunk_size: int = 500,
        is_hybrid_search: bool = True,
        sparse_top_k: int = 10,
        callback_manager: CallbackManager | None = None,
    ) -> None:
        self._llm = llm.get_model()
        self._embed_model = embeddings.get_model()
        self._vector_store = vector_store.get_client()
        self._document_data_mapper = document_data_mapper
        self.is_hybrid_search = is_hybrid_search
        self.sparse_top_k = sparse_top_k

        llama_debug = LlamaDebugHandler(print_trace_on_end=True)
        wandb_callback = WandbCallbackHandler(
            run_args={
                "project": "co-writer",
            }
        )
        callback_manager = CallbackManager([llama_debug, wandb_callback, CustomCallbackHandler()])

        self._service_context = ServiceContext.from_defaults(
            llm=self._llm,
            embed_model=self._embed_model,
            chunk_size=chunk_size,
            callback_manager=callback_manager,
        )
        self._storage_context = StorageContext.from_defaults(vector_store=self._vector_store)

        self._index = VectorStoreIndex.from_vector_store(
            self._vector_store,
            service_context=self._service_context,
        )

    def execute(self, query: str) -> str:
        hybrid_mode = "hybrid" if self.is_hybrid_search else "dense"
        self._query_engine = self._index.as_query_engine(
            service_context=self._service_context,
            vector_store_query_mode=hybrid_mode,
            sparse_top_k=self.sparse_top_k,
            similarity_top_k=self.sparse_top_k,
        )
        results = self._query_engine.query(query).response
        return results

    def index_documents(self, documents: list[Document]) -> None:
        llama_documents = [self._document_data_mapper.entity_to_model(doc) for doc in documents]
        for doc in tqdm(llama_documents):
            self._index.insert(doc, show_progress=True)

    def get_index(self) -> Any:
        return self._index

    def create_query_engine(
        self, prompt_template: Any, query_mode: str, top_k: int, response_mode: str
    ) -> Any:
        return self._index.as_query_engine(
            service_context=self._service_context,
            text_qa_template=prompt_template,
            vector_store_query_mode=query_mode,
            similarity_top_k=top_k,
            sparse_top_k=top_k,
            response_mode=response_mode,
        )


class CustomCallbackHandler(BaseCallbackHandler):
    def __init__(
        self,
        event_starts_to_ignore: Optional[list[CBEventType]] = None,
        event_ends_to_ignore: Optional[list[CBEventType]] = None,
        print_trace_on_end: bool = True,
    ) -> None:
        event_starts_to_ignore = event_starts_to_ignore if event_starts_to_ignore else []
        event_ends_to_ignore = event_ends_to_ignore if event_ends_to_ignore else []
        super().__init__(
            event_starts_to_ignore=event_starts_to_ignore,
            event_ends_to_ignore=event_ends_to_ignore,
        )

    def on_event_start(
        self,
        event_type: CBEventType,
        payload: Optional[dict[str, Any]] = None,
        event_id: str = "",
        parent_id: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        return event_id

    def on_event_end(
        self,
        event_type: CBEventType,
        payload: Optional[dict[str, Any]] = None,
        event_id: str = "",
        **kwargs: Any,
    ) -> None:
        if payload is not None and EventPayload.NODES in payload:
            nodes = payload[EventPayload.NODES]
            for node in nodes:
                print(node.node)
                print("\n\n")

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        pass

    def end_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[dict[str, list[str]]] = None,
    ) -> None:
        pass
