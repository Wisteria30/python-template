import logging.config  # noqa

from dependency_injector import containers, providers
from dependency_injector.wiring import inject  # noqa

from python_template.application.usecases import (
    CompletionUseCase,
    DiagnosticUseCase,
    DictionaryUseCase,
    DirectoryPreprocessingUseCase,
    DocumentPreprocessingUseCase,
    HoverUseCase,
    LlamaKnowledgeGraphUseCase,
    HeuristicDiagnosticUseCase,
    LlamaRagUseCase,
    NlpEntityUseCase,
    NotionPreprocessingUseCase,
    WordCompletionUseCase,
)
from python_template.config.settings import Settings
from python_template.domains.interfaces import (
    Embeddings,
    GraphStore,
    IDocumentDataMapper,
    IDocumentRepository,
    IMeaningRepository,
    INlpClient,
    INlpEntityRepository,
    IPageReader,
    Llm,
    VectorStore,
)
from python_template.domains.usecases import (
    ICompletionUseCase,
    IDiagnosticUseCase,
    IDictionaryUseCase,
    IDocumentPreprocessingUseCase,
    IHoverUseCase,
    IKnowledgeGraphUseCase,
    INlpEntityUseCase,
    IRagUseCase,
    IWordCompletionUseCase,
)
from python_template.infrastructures.interfaces import (
    DirectoryPageReader,
    DocumentDataMapper,
    FileDocumentRepository,
    GinzaNlpClient,
    LlamaAzureGpt4,
    LlamaGpt4,
    LlamaGpt4Turbo,
    LlamaGpt35Turbo,
    LlamaGptFineTune,
    LlamaGraphStore,
    LlamaNotionPageReader,
    LlamaOpenAIAda2Embeddings,
    LlamaPaLM,
    LlamaPGVector,
    MeaningRepository,
    NlpEntityRepository,
    YahooNlpClient,
)

from .database import Database
from .logging import set_logger


class Container(containers.DeclarativeContainer):
    """Dependency Injection Container

    see https://github.com/ets-labs/python-dependency-injector for more details
    """

    __self__ = providers.Self()

    settings = providers.Configuration(pydantic_settings=[Settings()])
    settings.load()

    set_logger(settings.LOG_LEVEL())

    db = providers.Singleton(Database, db_url=settings.POSTGRES_CONNECTION_STRING())

    # ================== Dependency injection to Interface ==================
    palm: providers.Provider[Llm] = providers.Factory(
        LlamaPaLM,
        gcp_project_id=settings.GCP_PROJECT_ID(),
        gcp_location=settings.GCP_LOCATION(),
        staging_bucket="gs://my_staging_bucket",
        credentials_path=settings.GCP_CREDENTIALS_PATH(),
        experiment="my-experiment",
        experiment_description="my experiment decsription",
    )

    azure_gpt4: providers.Provider[Llm] = providers.Factory(
        LlamaAzureGpt4,
        engine=settings.AZURE_OPENAI_GPT4_ENGINE(),
        endpoint_url=settings.AZURE_OPENAI_API_ENDPOINT_URL(),
        api_key=settings.AZURE_OPENAI_API_KEY(),
        api_version=settings.AZURE_OPENAI_API_VERSION(),
    )

    gpt4: providers.Provider[Llm] = providers.Factory(
        LlamaGpt4,
        api_key=settings.OPENAI_API_KEY(),
    )

    gpt4_turbo: providers.Provider[Llm] = providers.Factory(
        LlamaGpt4Turbo,
        api_key=settings.OPENAI_API_KEY(),
    )

    gpt35_turbo: providers.Provider[Llm] = providers.Factory(
        LlamaGpt35Turbo,
        api_key=settings.OPENAI_API_KEY(),
    )

    gpt_finetune: providers.Provider[Llm] = providers.Factory(
        LlamaGptFineTune,
        model=settings.OPENAI_FINE_TUNE_MODEL(),
        api_key=settings.OPENAI_API_KEY(),
    )

    # vertexai_embeddings: Embeddings = providers.Factory(
    #     LlamaVertexAiEmbeddings,
    #     gcp_project_id=settings.GCP_PROJECT_ID(),
    #     gcp_location=settings.GCP_LOCATION(),
    #     staging_bucket="gs://my_staging_bucket",
    #     credentials_path=settings.GCP_CREDENTIALS_PATH(),
    #     experiment="my-experiment",
    #     experiment_description="my experiment decsription",
    # )

    openai_ada2_embeddings: providers.Provider[Embeddings] = providers.Factory(
        LlamaOpenAIAda2Embeddings,
        api_key=settings.OPENAI_API_KEY(),
    )

    # vector_store: VectorStore = providers.Factory(
    #     LlamaWeaviate,
    #     weaviate_url=settings.WEAVIATE_URL(),
    # )

    vector_store: providers.Provider[VectorStore] = providers.Factory(
        LlamaPGVector,
        postgres_connection_string=settings.POSTGRES_CONNECTION_STRING(),
        table_name=settings.VECTOR_STORE_TABLE_NAME(),
        embed_dim=settings.EMBED_DIM(),
        is_hybrid_search=settings.IS_HYBRID_SEARCH(),
        text_search_config=settings.TEXT_SEARCH_CONFIG(),
    )

    graph_store: providers.Provider[GraphStore] = providers.Factory(
        LlamaGraphStore,
        persist_dir=settings.KNOWLEDGE_GRAPH_PERSIST_DIR(),
    )

    # neo4j_graph_store: GraphStore = providers.Factory(
    #     LlamaNeo4j,
    #     username=settings.NEO4J_USER(),
    #     password=settings.NEO4J_PASSWORD(),
    #     url=settings.NEO4J_URL(),
    #     database=settings.NEO4J_DATABASE(),
    # )

    nlp_entity_repository: providers.Provider[INlpEntityRepository] = providers.Factory(
        NlpEntityRepository,
        session_factory=db.provided.session,
    )

    meaning_repository: providers.Provider[IMeaningRepository] = providers.Factory(
        MeaningRepository,
        session_factory=db.provided.session,
    )

    ginza_nlp_client: providers.Provider[INlpClient] = providers.Factory(
        GinzaNlpClient,
    )
    yahoo_nlp_client: providers.Provider[INlpClient] = providers.Factory(
        YahooNlpClient,
        client_id=settings.YAHOO_CLIENT_ID(),
    )

    document_data_mapper: providers.Provider[IDocumentDataMapper] = providers.Factory(
        DocumentDataMapper,
    )

    document_repository: providers.Provider[IDocumentRepository] = providers.Factory(
        FileDocumentRepository,
        path=settings.DOCUMENTS_PATH(),
    )

    notion_page_reader: providers.Provider[IPageReader] = providers.Factory(
        LlamaNotionPageReader,
        notion_integration_token=settings.NOTION_INTEGRATION_TOKEN(),
        document_data_mapper=document_data_mapper,
    )

    directory_page_reader: providers.Provider[IPageReader] = providers.Factory(
        DirectoryPageReader,
        document_data_mapper=document_data_mapper,
    )

    # ================== Dependency injection to Application ==================
    llama_palm_rag_usecase: providers.Provider[IRagUseCase] = providers.Factory(
        LlamaRagUseCase,
        llm=palm,
        embeddings=openai_ada2_embeddings,
        vector_store=vector_store,
        document_data_mapper=document_data_mapper,
        chunk_size=settings.CHUNK_SIZE(),
        is_hybrid_search=settings.IS_HYBRID_SEARCH(),
        sparse_top_k=5,
    )

    llama_gpt4_rag_usecase: providers.Provider[IRagUseCase] = providers.Factory(
        LlamaRagUseCase,
        llm=gpt4,
        embeddings=openai_ada2_embeddings,
        vector_store=vector_store,
        document_data_mapper=document_data_mapper,
        chunk_size=settings.CHUNK_SIZE(),
        is_hybrid_search=settings.IS_HYBRID_SEARCH(),
        sparse_top_k=5,
    )

    llama_gpt35_turbo_rag_usecase: providers.Provider[IRagUseCase] = providers.Factory(
        LlamaRagUseCase,
        llm=gpt35_turbo,
        embeddings=openai_ada2_embeddings,
        vector_store=vector_store,
        document_data_mapper=document_data_mapper,
        chunk_size=settings.CHUNK_SIZE(),
        is_hybrid_search=settings.IS_HYBRID_SEARCH(),
        sparse_top_k=5,
    )

    llama_gpt4_knowledge_graph_usecase: providers.Provider[
        IKnowledgeGraphUseCase
    ] = providers.Factory(
        LlamaKnowledgeGraphUseCase,
        llm=gpt4,
        embeddings=openai_ada2_embeddings,
        graph_store=graph_store,
        document_data_mapper=document_data_mapper,
        is_hybrid_search=settings.IS_HYBRID_SEARCH(),
        sparse_top_k=5,
        persist_dir=settings.KNOWLEDGE_GRAPH_PERSIST_DIR(),
    )

    llama_gpt35_turbo_knowledge_graph_usecase: providers.Provider[
        IKnowledgeGraphUseCase
    ] = providers.Factory(
        LlamaKnowledgeGraphUseCase,
        llm=gpt35_turbo,
        embeddings=openai_ada2_embeddings,
        graph_store=graph_store,
        document_data_mapper=document_data_mapper,
        is_hybrid_search=settings.IS_HYBRID_SEARCH(),
        sparse_top_k=5,
        persist_dir=settings.KNOWLEDGE_GRAPH_PERSIST_DIR(),
    )

    nlp_entity_usecase: providers.Provider[INlpEntityUseCase] = providers.Factory(
        NlpEntityUseCase,
        repository=nlp_entity_repository,
        nlp_client=ginza_nlp_client,
    )

    dictionary_usecase: providers.Provider[IDictionaryUseCase] = providers.Factory(
        DictionaryUseCase,
        meaning_repository=meaning_repository,
        nlp_entity_repository=nlp_entity_repository,
        rag_usecase=llama_gpt4_rag_usecase,
        is_hybrid_search=settings.IS_HYBRID_SEARCH(),
        sparse_top_k=5,
    )

    diagnostics_usecase: providers.Provider[IDiagnosticUseCase] = providers.Factory(
        DiagnosticUseCase,
        llm=gpt4,
        embeddings=openai_ada2_embeddings,
        rag_usecase=llama_gpt4_rag_usecase,
        sparse_top_k=7,
    )
    heuristic_diagnostics_usecase: providers.Provider[IDiagnosticUseCase] = providers.Factory(
        HeuristicDiagnosticUseCase,
        nlp_client=yahoo_nlp_client,
    )

    completion_usecase: providers.Provider[ICompletionUseCase] = providers.Factory(
        CompletionUseCase,
        # llm=gpt_finetune,
        llm=gpt4_turbo,
    )

    word_completion_usecase: providers.Provider[IWordCompletionUseCase] = providers.Factory(
        WordCompletionUseCase,
        nlp_entity_repository=nlp_entity_repository,
        nlp_client=ginza_nlp_client,
    )

    document_preprocessing_usecase: providers.Provider[
        IDocumentPreprocessingUseCase
    ] = providers.Factory(
        DocumentPreprocessingUseCase,
        document_repository=document_repository,
        dictionary_usecase=dictionary_usecase,
        nlp_entity_usecase=nlp_entity_usecase,
        rag_usecase=llama_gpt35_turbo_rag_usecase,
    )

    directory_preprocessing_usecase: providers.Provider[
        IDocumentPreprocessingUseCase
    ] = providers.Factory(
        DirectoryPreprocessingUseCase,
        page_reader=directory_page_reader,
        document_repository=document_repository,
        dictionary_usecase=dictionary_usecase,
        nlp_entity_usecase=nlp_entity_usecase,
        rag_usecase=llama_gpt35_turbo_rag_usecase,
    )

    notion_preprocessing_usecase: providers.Provider[
        IDocumentPreprocessingUseCase
    ] = providers.Factory(
        NotionPreprocessingUseCase,
        notion_page_reader=notion_page_reader,
        nlp_entity_usecase=nlp_entity_usecase,
        rag_usecase=llama_gpt35_turbo_rag_usecase,
        knowledge_graph_usecase=llama_gpt4_knowledge_graph_usecase,
    )

    hover_usecase: providers.Provider[IHoverUseCase] = providers.Factory(
        HoverUseCase,
        meaning_repository=meaning_repository,
        nlp_entity_repository=nlp_entity_repository,
        nlp_client=ginza_nlp_client,
    )
