import pathlib


def get_root():
    return pathlib.Path('.').resolve()


ROOT_PATH = get_root()
DATA_PATH = ROOT_PATH / 'data'
MODELS_PATH = ROOT_PATH / 'models'
SRC_PATH = ROOT_PATH / 'src'
