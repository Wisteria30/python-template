from python_template.domains.interfaces import Embeddings
from google.cloud import aiplatform
from google.oauth2 import service_account
from langchain.embeddings import VertexAIEmbeddings
from llama_index.embeddings import LangchainEmbedding


class LlamaVertexAiEmbeddings(Embeddings):
    def __init__(
        self,
        gcp_project_id: str,
        gcp_location: str,
        staging_bucket: str,
        credentials_path: str,
        experiment: str,
        experiment_description: str,
    ) -> None:
        # 認証情報オブジェクトを作成
        my_credentials = (
            service_account.Credentials.from_service_account_file(credentials_path)
            if credentials_path
            else None
        )
        aiplatform.init(
            project=gcp_project_id,
            location=gcp_location,
            staging_bucket=staging_bucket,
            credentials=my_credentials,
            # encryption_spec_key_name=my_encryption_key_name,  # moreでKMSやる
            experiment=experiment,
            experiment_description=experiment_description,
        )
        self._model = LangchainEmbedding(VertexAIEmbeddings())

    def get_model(self) -> object:
        return self._model
