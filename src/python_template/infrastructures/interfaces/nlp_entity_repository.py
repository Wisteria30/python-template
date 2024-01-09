from contextlib import AbstractContextManager
from typing import TYPE_CHECKING, Callable

from python_template.config.database import Base
from python_template.domains.entities import NlpEntity
from python_template.domains.interfaces import INlpEntityRepository
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, Session, relationship

if TYPE_CHECKING:
    from .meaning_repository import MeaningModel


class NlpEntityModel(Base):
    __tablename__ = "nlp_entity"
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    word: Mapped[str] = Column(String, nullable=False, index=True)
    label: Mapped[str] = Column(String, nullable=False)
    frequency: Mapped[int] = Column(Integer, nullable=False, default=0)
    meaning: Mapped["MeaningModel"] = relationship(back_populates="entity")


class NlpEntityDataMapper:
    @staticmethod
    def model_to_entity(instance: NlpEntityModel) -> NlpEntity:
        return NlpEntity(
            id=instance.id,
            word=instance.word,
            label=instance.label,
            frequency=instance.frequency,
        )

    @staticmethod
    def entity_to_model(entity: NlpEntity) -> NlpEntityModel:
        return NlpEntityModel(
            id=entity.id,
            word=entity.word,
            label=entity.label,
            frequency=entity.frequency,
        )


class NlpEntityRepository(INlpEntityRepository):
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[Session]],
    ) -> None:
        self.session_factory = session_factory
        self.model_class = NlpEntityModel
        self.mapper_class = NlpEntityDataMapper

    def add(self, entity: NlpEntity) -> None:
        with self.session_factory() as session:
            model = self.mapper_class.entity_to_model(entity)
            session.add(model)
            session.commit()
            session.refresh(model)

    def update(self, entity: NlpEntity) -> None:
        with self.session_factory() as session:
            model = self.mapper_class.entity_to_model(entity)
            session.merge(model)
            session.commit()
            return self.mapper_class.model_to_entity(model)

    def save(self, entity: NlpEntity) -> None:
        # entity.wordが存在する場合はupdate、存在しない場合はadd
        model = self.find_by_word(entity.word)
        if model is None:
            self.add(entity)
        else:
            new_entity = self.mapper_class.model_to_entity(model)
            new_entity.frequency += entity.frequency
            self.update(new_entity)

    def delete(self, entity: NlpEntity) -> None:
        with self.session_factory() as session:
            model = self.mapper_class.entity_to_model(entity)
            session.delete(model)
            session.commit()
            return self.mapper_class.model_to_entity(model)

    def find_by_id(self, entity_id: int) -> NlpEntity | None:
        with self.session_factory() as session:
            model = session.query(self.model_class).filter_by(id=entity_id).first()
            if model is None:
                return None
            return self.mapper_class.model_to_entity(model)

    def find_by_word(self, word: str) -> NlpEntity | None:
        with self.session_factory() as session:
            model = session.query(self.model_class).filter_by(word=word).first()
            if model is None:
                return None
            return self.mapper_class.model_to_entity(model)

    def find_all(self) -> list[NlpEntity]:
        with self.session_factory() as session:
            models = (
                session.query(self.model_class).order_by(self.model_class.frequency.desc()).all()
            )
            entities = [self.mapper_class.model_to_entity(model) for model in models]
            return entities

    def search(self, query: str) -> list[NlpEntity]:
        """%LIKE%で検索して、frequencyの降順で返す"""
        with self.session_factory() as session:
            models = (
                session.query(self.model_class)
                .filter(self.model_class.word.like(f"{query}%"))
                .order_by(self.model_class.frequency.desc())
                .all()
            )
            print(models)
            entities = [self.mapper_class.model_to_entity(model) for model in models]
            return entities

    def __getitem__(self, key: int) -> NlpEntity | None:
        return self.find_by_id(key)
