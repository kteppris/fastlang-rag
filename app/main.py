from fastapi import FastAPI
from dotenv import load_dotenv
import logging

from api import router as api_router
from conf.config import get_config
from retriever.vectorstore_factory import VectorstoreFactory
from retriever.encoder_factory import EncoderFactory
from retriever.ingest import ingest_documents
from reader.reader_factory import ReaderFactory

app = FastAPI()

app.include_router(api_router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    # Load environment variables from .env file
    load_dotenv()
    config = get_config()

    encoder = EncoderFactory.get_encoder(config)
    vectorstore = VectorstoreFactory.get_vectorstore(config, encoder)
    ingest_documents(config, vectorstore)
    app.state.vectorstore = vectorstore
    app.state.qa_chain = ReaderFactory.get_chain(
        config=config, 
        retriever=vectorstore.as_retriever(**config.vectorstore.search_args)
    )
    logger.info("API startup successful")
    