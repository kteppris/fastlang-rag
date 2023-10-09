from omegaconf import OmegaConf
from langchain.vectorstores.base import VectorStore

from .loader.document_loader import DocumentLoader

def ingest_documents(config: OmegaConf, vectorstore: VectorStore) -> None:
    # TODO: ingest only changed/new documents
    loader = DocumentLoader(config)
    docs = loader.load_documents()
    vectorstore.add_documents(docs)
