import asyncio
import logging

from typing import Literal

from python_template.domains.entities import (
    Diagnostic,
    Diagnostics,
    DiagnosticsInput,
    Position,
    Range,
)
from python_template.domains.interfaces import Embeddings, Llm
from python_template.domains.usecases import IDiagnosticUseCase, IRagUseCase
from llama_index import ServiceContext
from llama_index.callbacks import CallbackManager, LlamaDebugHandler, WandbCallbackHandler
from llama_index.prompts import ChatMessage, ChatPromptTemplate, MessageRole
from llama_index.response.schema import PydanticResponse
from llama_index.text_splitter import TokenTextSplitter
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class DiagnosticUseCase(IDiagnosticUseCase):
    def __init__(
        self,
        llm: Llm,
        embeddings: Embeddings,
        rag_usecase: IRagUseCase,
        chunk_size: int = 512,
        is_hybrid_search: bool = True,
        sparse_top_k: int = 10,
        callback_manager: CallbackManager | None = None,
    ) -> None:
        self._llm = llm.get_model()
        self._embed_model = embeddings.get_model()
        self._index = rag_usecase.get_index()
        self._text_splitter = TokenTextSplitter(chunk_size=4096, chunk_overlap=128, separator="。")

        chat_template = ChatPromptTemplate(
            message_templates=[
                ChatMessage(
                    role=MessageRole.SYSTEM,
                    content=self._system_message(),
                ),
                ChatMessage(
                    role=MessageRole.USER,
                    content="Here are some additional context:\n{context_str}",
                ),
                ChatMessage(
                    role=MessageRole.USER,
                    content="{query_str}",
                ),
            ]
        )

        if callback_manager is None:
            llama_debug = LlamaDebugHandler(print_trace_on_end=True)
            wandb_callback = WandbCallbackHandler(
                run_args={
                    "project": "co-writer",
                }
            )
            callback_manager = CallbackManager([llama_debug, wandb_callback])

        self._service_context = ServiceContext.from_defaults(
            llm=self._llm,
            embed_model=self._embed_model,
            chunk_size=chunk_size,
            callback_manager=callback_manager,
        )
        hybrid_mode = "hybrid" if is_hybrid_search else "dense"
        self._query_engine = self._index.as_query_engine(
            service_context=self._service_context,
            text_qa_template=chat_template,
            vector_store_query_mode=hybrid_mode,
            similarity_top_k=sparse_top_k,
            sparse_top_k=sparse_top_k,
            response_mode="compact",
            output_cls=_RawLlmDiagnostics,
        )

    async def execute(self, input_: DiagnosticsInput) -> Diagnostics:
        async def handle_query(query: str) -> list[Diagnostic]:
            try:
                response: PydanticResponse = await asyncio.to_thread(
                    self._query_engine.query, query
                )
                diagnostics = _RawLlmDiagnostics.validate(response.response)
                return [_convert(diagnostic, doc) for diagnostic in diagnostics.diagnostics]
            except Exception as e:
                raise e

        doc = input_.current_doc.content
        queries = self._query_strs(input_)
        diagnostics_list = Diagnostics(diagnostics=[])

        results = await asyncio.gather(
            *(handle_query(query) for query in queries), return_exceptions=True
        )
        for result in results:
            if isinstance(result, Exception):
                logger.error(result, exc_info=True)
                continue
            diagnostics_list.diagnostics.extend(result)

        return diagnostics_list

    def _query_strs(self, input_: DiagnosticsInput) -> list[str]:
        if input_.instruction == "":
            instruction = ""
        else:
            instruction = f"Instruction: {input_.instruction}\n"

        chunk_queries = []
        for chunk in self._text_splitter.split_text(input_.current_doc.content):
            chunk_queries.append(f"{instruction}## Document to be reviewed\n{chunk}")

        return chunk_queries

    def _system_message(self) -> str:
        language = "日本語"
        return f"""You are a professional document reviewer. Spot problems in the given document, including but not limtied to:
- Grammatical errors, typos or bad formatting.
- Incosistency with the given context information.
- Keep the reviews to 5 in order of importance.

You must answer in ${language}. If you find no problems, just return an empty list.
"""


class _RawLlmDiagnostic(BaseModel):
    problematic_part: str
    message: str
    severity: Literal["error", "warn", "info", "hint"]


class _RawLlmDiagnostics(BaseModel):
    """文章の中の問題点"""

    # この docstring は Llama Index の Pydantic Outputs に使用されるため、ランタイム動作に影響する。
    # 編集/削除する場合は注意。

    diagnostics: list[_RawLlmDiagnostic]


def _convert(diagnostic: _RawLlmDiagnostic, document: str) -> Diagnostic:
    return Diagnostic(
        message=diagnostic.message,
        severity=diagnostic.severity,
        range=_get_range_in(diagnostic.problematic_part, document),
    )


def _get_range_in(part: str, document: str) -> Range:
    start = document.find(part)
    end = start + len(part)
    return Range(
        start=Position.create_from_index(document, start),
        end=Position.create_from_index(document, end),
    )
