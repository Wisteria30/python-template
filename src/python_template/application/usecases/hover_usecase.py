from python_template.domains.entities import HoverInfo, HoverInput
from python_template.domains.interfaces import IMeaningRepository, INlpClient, INlpEntityRepository
from python_template.domains.usecases import IHoverUseCase


class HoverUseCase(IHoverUseCase):
    def __init__(
        self,
        meaning_repository: IMeaningRepository,
        nlp_entity_repository: INlpEntityRepository,
        nlp_client: INlpClient,
    ) -> None:
        self.meaning_repository = meaning_repository
        self.nlp_entity_repository = nlp_entity_repository
        self.nlp_client = nlp_client

    def execute(self, input_data: HoverInput) -> HoverInfo:
        """
        1. インプットから現在の単語を取得する
        1. 単語の定義を検索する
        2. 生成された文言を用意する
        3. 関連ページのURLを生成（Notionはpage_idのハイフンを削除したものをhttps://www.notion.so/につけると見れる）
        4. ラップして返す
        """
        content = input_data.current_doc.content
        position = input_data.current_doc.position
        text, range_ = self.nlp_client.get_morpheme_by_position(content, position)
        # Top2ぐらいは表記揺れで補完になりそう
        entities = self.nlp_entity_repository.search(text)[:2][::-1]
        explanations: str = ""
        for entity in entities:
            meaning = self.meaning_repository.find_by_entity_id(entity.id)
            if meaning is None:
                continue
            explanations += f"### {entity.word}\n*{meaning.meaning}*\n\n"
        # entityが見つからなかった場合は回答できない
        if explanations == "":
            explanations = "説明することができませんでした。"

        hover_info = HoverInfo(text=explanations, range=range_)
        return hover_info

    def get_url(document) -> str:
        host_url = "https://www.notion.so/"
        page_id = document.metadata["page_id"]
        formatted_page_id = page_id.replace("-", "")
        url = f"{host_url}{formatted_page_id}"
        return url
