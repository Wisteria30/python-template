from typing import Any

from python_template.domains.entities.documents import Document
from python_template.domains.interfaces import IDocumentDataMapper
from llama_index import Document as LlamaDocument


class DocumentDataMapper(IDocumentDataMapper):
    @staticmethod
    def model_to_entity(instance: Any) -> Document:
        if not isinstance(instance, LlamaDocument):
            raise TypeError(f"instance must be LlamaDocument, but {type(instance)} was given")
        dict_instance = instance.to_dict()
        return Document(
            id=dict_instance["id_"],
            embedding=dict_instance["embedding"],
            metadata=dict_instance["metadata"],
            excluded_embed_metadata_keys=dict_instance["excluded_embed_metadata_keys"],
            excluded_llm_metadata_keys=dict_instance["excluded_llm_metadata_keys"],
            relationships=dict_instance["relationships"],
            hash=dict_instance["hash"],
            text=dict_instance["text"],
            start_char_idx=dict_instance["start_char_idx"],
            end_char_idx=dict_instance["end_char_idx"],
            text_template=dict_instance["text_template"],
            metadata_template=dict_instance["metadata_template"],
            metadata_seperator=dict_instance["metadata_seperator"],
            class_name=dict_instance["class_name"],
        )

    @staticmethod
    def entity_to_model(entity: Document) -> Any:
        dict_entity = entity.dict()
        return LlamaDocument(**dict_entity)
