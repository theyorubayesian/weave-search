from copy import deepcopy
from itertools import product
from typing import Dict
from typing import List
from typing import Union

from docarray import Document
from docarray import DocumentArray
from docarray.array.weaviate import WeaviateConfig
from jina import Executor 
from jina import requests

from .data_utils import get_information_for_term


class SemanticSearchExecutor(Executor):
    def __init__(
        self, 
        model_name: str, 
        data_categories: List[str], 
        subcategories: List[str], 
        weaviate_config: Dict[str, Union[int, str]], 
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.model_name = model_name
        self.encoder = Executor.from_hub(
            "jinahub://TransformerSentenceEncoder",
            uses_with={
                "model_name": model_name,
            }
        )
        self.data_categories = data_categories
        self.subcategories = subcategories
        
        cfg = WeaviateConfig(**weaviate_config)
        self.all_docs = DocumentArray(storage='weaviate', config=cfg)
        self.all_docs.summary()

    @requests(on="/add_documents")
    def add_documents(self, docs: DocumentArray, **kwargs):
        self._encode_documents(docs)
        self.all_docs.extend(docs)
    
    @requests(on="/add_documents_from_terms")
    def add_documents_from_terms(self, docs: DocumentArray, **kwargs):
        all_docs = self.get_documents_from_terms(docs.texts)
        self.add_documents(all_docs)
    
    @requests(on="/find_documents")
    def find_documents(self, docs: DocumentArray, **kwargs):
        self._encode_documents(docs)
        results = self.all_docs.find(docs, limit=1)
        return results[0]

    @staticmethod
    def create_biodocument(item: dict) -> Document:
        """
        Convert item dictionary to BiomedicalDocument dataclass
        Args:
            item (dict): item dictionary
        Returns:
            BiomedicalDocument: BiomedicalDocument dataclass
        """
        doc = Document(
            dbId=item.get("dbId", ""),
            stId=item.get("stId", ""),
            _id=item.get("id", ""),
            name=item.get("name", ""),
            exactType=item.get("exactType", ""),
            species=item.get("species", []),
            referenceName=item.get("referenceName", ""),
            referenceIdentifier=item.get("referenceIdentifier", ""),
            compartmentNames=item.get("compartmentNames", []),
            compartmentAccession=item.get("compartmentAccession", []),
            isDisease=item.get("isDisease", False),
            databaseName=item.get("databaseName", ""),
            referenceURL=item.get("referenceURL", ""),
            text=item.get("summation", ""),
        )
        return doc

    def get_documents_from_terms(self, terms: List[str]) -> DocumentArray:
        all_data = {term: get_information_for_term(term) for term in terms}
        all_docs = []
        
        for term, category, sub_category in product(
            *[terms, self.data_categories, self.subcategories], repeat=1):
            doc: Union[list, dict] = all_data[term][category][sub_category]
            
            doc_list = deepcopy(doc)
            if not isinstance(doc_list, list):
                doc_list = doc.values()

            term_docs = []
            for item in doc_list:
                if "summation" in item:
                    term_docs.append(self.create_biodocument(item))

            all_docs.extend(term_docs)
            
        return DocumentArray(all_docs)
    
    def _encode_documents(self, doc_list: DocumentArray, **kwargs) -> DocumentArray:
        self.encoder.encode(doc_list)
