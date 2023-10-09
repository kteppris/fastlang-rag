from omegaconf import OmegaConf
import importlib
import logging
import datetime
from langchain.document_loaders import PyPDFLoader
from .splitter import init_splitters

logger = logging.getLogger(__name__)

class DocumentLoader:
    """
    Loads documents based on the provided configuration, and optionally splits the content as specified.
    """
    def __init__(self, config) -> None:
        self.config = config

    def load_documents(self) -> dict:
        """
        Load and optionally split documents based on the configuration.

        Returns
        -------
        dict
            A dictionary of loaded documents, each enhanced with metadata such as source, fetch time, and encoder model.

        Notes
        -----
        The method skips sources for which the loader could not be initialized. Each document's content may be split 
        based on specified splitters in the configuration.
        """
        loaded_docs = []
        text_splitters = init_splitters(self.config)

        for source_name, source_details in self.config.data.sources.items():
            source_type = source_details.type

            loader = self._init_loader(source_type, **source_details.args)

            if not loader:
                continue  # If loader could not be initialized, skip to the next source.

            splitter = text_splitters.get(source_details.content_type)

            if splitter:
                docs = loader.load_and_split(splitter)
            else:
                docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = source_name
                doc.metadata["file_path"] = source_details.args.get("file_path", None)
                doc.metadata["fetch_time"] = datetime.datetime.now().isoformat()
                doc.metadata["encoder_model"] = self.config.encoder.name

        loaded_docs.extend(docs)
        return loaded_docs

    def _init_loader(self, loader_type, **kwargs):
        """
        Initializes and returns the appropriate document loader based on the type.

        Parameters
        ----------
        loader_type : str
            The type of document loader to initialize.
        **kwargs : dict
            Additional keyword arguments to pass to the loader's initialization.

        Returns
        -------
        Any
            An instance of the document loader or None if initialization failed.
        """
        try:
            module = importlib.import_module("langchain.document_loaders")
            LoaderClass = getattr(module, loader_type)
            return LoaderClass(**kwargs)
        except AttributeError:
            logger.error(f"Loader {loader_type} is not found in langchain.document_loaders module.")
            return None
        except ImportError:
            logger.error(f"Error importing langchain.document_loaders module.")
            return None