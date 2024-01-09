import logging

from textwrap import dedent

from python_template.domains.entities import Meaning, NlpEntity
from python_template.domains.interfaces import (
    IMeaningRepository,
    INlpEntityRepository,
)
from python_template.domains.usecases import IDictionaryUseCase, IRagUseCase
from llama_index.prompts import ChatMessage, ChatPromptTemplate, MessageRole
from tqdm import tqdm

logger = logging.getLogger(__name__)


class DictionaryUseCase(IDictionaryUseCase):
    def __init__(
        self,
        meaning_repository: IMeaningRepository,
        nlp_entity_repository: INlpEntityRepository,
        rag_usecase: IRagUseCase,
        is_hybrid_search: bool = True,
        sparse_top_k: int = 5,
    ) -> None:
        self._meaning_repository = meaning_repository
        self._nlp_entity_repository = nlp_entity_repository
        self._rag_usecase = rag_usecase

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
                    content="## Explaining words: \n{query_str}\n\n",
                ),
            ]
        )

        hybrid_mode = "hybrid" if is_hybrid_search else "dense"
        self._query_engine = self._rag_usecase.create_query_engine(
            chat_template,
            hybrid_mode,
            sparse_top_k,
            "compact",
        )

    def execute(self) -> None:
        entities: list[NlpEntity] = self._nlp_entity_repository.find_all()
        # entities = entities[:200]
        entities = [entity for entity in entities if entity.frequency >= 2]
        for entity in tqdm(entities):
            response = self._query_engine.query(entity.word)
            if response is None:
                continue
            answer = response.response
            logger.info(f"{entity.word}: {answer}")
            meaning = Meaning.create(
                word=entity.word,
                meaning=answer,
                entity_id=entity.id,
            )
            self._meaning_repository.save(meaning)

    def _system_message(self) -> str:
        language = "Japanese"

        return dedent(
            f"""You are a professional dictionary editor working for a publishing company. Consider and compile the meanings of the given words in additional contexts.
            When compiling, please have the following items in mind and generate a summary of them. Do not use bullet points.
            - Description, Name, Position/Role, Related Projects/Requests, Contacts/Involved Parties, Examples of Use, Related Terms

            You must answer in ${language}. If the meaning of a word cannot be explained, return only "この言葉は説明することができませんでした"
            """
        )
