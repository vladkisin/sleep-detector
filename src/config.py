import pathlib
from src.common import InputKeys, AggTransforms


def get_root():
    return pathlib.Path('.').resolve().parents[0]


ROOT_PATH = get_root()
DATA_PATH = ROOT_PATH / 'data'
SRC_PATH = ROOT_PATH / 'src'

input_keys = InputKeys()
agg_trns = AggTransforms(input_keys=input_keys)
