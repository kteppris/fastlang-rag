from omegaconf import OmegaConf
import importlib
import logging

def init_splitters(config: OmegaConf) -> dict:
    """
    Factory method to initialize and fetch text splitters based on the provided configuration.

    Each content type in the sources must have a corresponding text splitter defined.
    
    Example:
    -------
    ```yaml
    sources:
      gruenderwiki:
        type: 'online_pdf'
        content_type: 'text'
        ...

    splitter:
      text: 
        type: RecursiveCharacterTextSplitter
        ...
    ```
    In this example, the content type 'text' in the sources has a corresponding text splitter defined in the splitter section.

    Parameters
    ----------
    config : OmegaConf
        Configuration detailing the sources and their respective splitters, including their types and initialization parameters.

    Returns
    -------
    dict
        A dictionary containing initialized text splitter instances for each content type. 
        The key is the content type and the value is the corresponding splitter instance or `None` if the splitter could not be found or initialized.

    Notes
    -----
    The function logs warnings and errors in case of missing splitters or import issues but does not raise exceptions.
    """
    splitters = {}
    required_splitters = set()

    # Identify which splitters are required
    for source_name, source_conf in config.data.sources.items():
        required_splitters.add(source_conf.content_type)

    # Initialize and store required splitters
    for required_splitter in required_splitters:
        if required_splitter in config.data.splitter:
            split_conf = config.data.splitter[required_splitter]

            # Dynamically import the required splitter class
            try:
                module = importlib.import_module("langchain.text_splitter")
                SplitterClass = getattr(module, split_conf.type)
                
                # Instantiate the class with the provided arguments
                args = {} if not split_conf.args else split_conf.args
                splitter_instance = SplitterClass(**args)

                # Save the instance in the dictionary
                splitters[required_splitter] = splitter_instance

            except ImportError:
                logging.warning(f"The splitter '{split_conf.type}' could not be found in 'langchain.text_splitter'. Skipping.")
                splitters[required_splitter] = None
        else:
            logging.error(f"No splitter defined for content type '{required_splitter}'.")
            splitters[required_splitter] = None

    return splitters
