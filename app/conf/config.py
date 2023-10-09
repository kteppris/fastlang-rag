from hydra import compose, initialize
from omegaconf import OmegaConf

def get_config() -> OmegaConf:
    with initialize(version_base=None, config_path="."):
        cfg = compose(config_name="config.yaml")
    return cfg

if __name__ == '__main__':
    cfg = get_config()