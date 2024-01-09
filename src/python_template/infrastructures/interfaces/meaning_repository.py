from contextlib import AbstractContextManager
from typing import TYPE_CHECKING, Callable

from python_template.config.database import Base
from python_template.domains.entities import Meaning
from python_template.domains.interfaces import IMeaningRepository
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, Session, relationship

if TYPE_CHECKING:
    from .nlp_entity_repository import NlpEntityModel


class MeaningModel(Base):
    __tablename__ = "meaning"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    word: Mapped[str] = Column(String, nullable=False, index=True)
    meaning: Mapped[str] = Column(String, nullable=False)
    entity_id: Mapped[int] = Column(
        Integer,
        ForeignKey("nlp_entity.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=True,
        index=True,
        default=None,
    )
    entity: Mapped["NlpEntityModel"] = relationship(back_populates="meaning")


class MeaningDataMapper:
    @staticmethod
    def model_to_entity(instance: MeaningModel) -> Meaning:
        return Meaning(
            id=instance.id,
            word=instance.word,
            meaning=instance.meaning,
            entity_id=instance.entity_id,
        )

    @staticmethod
    def entity_to_model(entity: Meaning) -> MeaningModel:
        return MeaningModel(
            id=entity.id,
            word=entity.word,
            meaning=entity.meaning,
            entity_id=entity.entity_id,
        )


class MeaningRepository(IMeaningRepository):
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[Session]],
    ) -> None:
        self.session_factory = session_factory
        self.model_class = MeaningModel
        self.mapper_class = MeaningDataMapper

    def add(self, entity: Meaning) -> None:
        with self.session_factory() as session:
            model = self.mapper_class.entity_to_model(entity)
            session.add(model)
            session.commit()
            session.refresh(model)

    def update(self, entity: Meaning) -> None:
        with self.session_factory() as session:
            model = self.mapper_class.entity_to_model(entity)
            session.merge(model)
            session.commit()
            return self.mapper_class.model_to_entity(model)

    def save(self, entity: Meaning) -> None:
        # entity.wordが存在する場合はupdate、存在しない場合はadd
        model = self.find_by_word(entity.word)
        if model is None:
            self.add(entity)
        else:
            self.update(entity)

    def delete(self, entity: Meaning) -> None:
        with self.session_factory() as session:
            model = self.mapper_class.entity_to_model(entity)
            session.delete(model)
            session.commit()
            return self.mapper_class.model_to_entity(model)

    def find_by_id(self, entity_id: int) -> Meaning | None:
        with self.session_factory() as session:
            model = session.query(self.model_class).filter_by(id=entity_id).first()
            if model is None:
                return None
            return self.mapper_class.model_to_entity(model)

    def find_by_word(self, word: str) -> Meaning | None:
        with self.session_factory() as session:
            model = session.query(self.model_class).filter_by(word=word).first()
            if model is None:
                return None
            return self.mapper_class.model_to_entity(model)

    def find_by_entity_id(self, entity_id: int) -> Meaning | None:
        with self.session_factory() as session:
            model = (
                session.query(self.model_class)
                .filter(self.model_class.entity_id == entity_id)
                .first()
            )
            if model is None:
                return None
            return self.mapper_class.model_to_entity(model)

    def find_all(self) -> list[Meaning]:
        with self.session_factory() as session:
            models = session.query(self.model_class).all()
            entities = [self.mapper_class.model_to_entity(model) for model in models]
            return entities

    def search(self, query: str) -> list[Meaning]:
        """%LIKE%で検索して返す"""
        with self.session_factory() as session:
            models = (
                session.query(self.model_class)
                .filter(self.model_class.word.like(f"{query}%"))
                .all()
            )
            print(models)
            entities = [self.mapper_class.model_to_entity(model) for model in models]
            return entities

    def __getitem__(self, key: int) -> Meaning | None:
        return self.find_by_id(key)
