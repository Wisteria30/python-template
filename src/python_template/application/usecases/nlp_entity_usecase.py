from python_template.domains.interfaces import INlpClient, INlpEntityRepository
from python_template.domains.usecases import INlpEntityUseCase
from tqdm import tqdm


class NlpEntityUseCase(INlpEntityUseCase):
    def __init__(self, repository: INlpEntityRepository, nlp_client: INlpClient) -> None:
        self.repository = repository
        self.nlp_client = nlp_client

    def execute(self, text: str) -> None:
        entities = self.nlp_client.extract_entities(text)
        for entity in tqdm(entities):
            self.repository.save(entity)
