from python_template.domains.entities import Completion, Position
from python_template.domains.interfaces import INlpClient, INlpEntityRepository
from python_template.domains.usecases import IWordCompletionUseCase


class WordCompletionUseCase(IWordCompletionUseCase):
    def __init__(self, nlp_entity_repository: INlpEntityRepository, nlp_client: INlpClient) -> None:
        self.nlp_entity_repository = nlp_entity_repository
        self.nlp_client = nlp_client

    def execute(self, content: str, position: Position) -> list[Completion]:
        """指定した位置の単語を元に補完候補を返す"""
        text, range_ = self.nlp_client.get_morpheme_by_position(content, position)
        entities = self.nlp_entity_repository.search(text)
        completions = [Completion.create(entity.word, range_) for entity in entities]
        # 上位5件のみ返す
        return completions[:5]
