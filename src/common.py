import pickle
from dataclasses import dataclass, field
from typing import List, Tuple
from src.config import MODELS_PATH


@dataclass
class InputKeys:
    PRIMARY_KEY: str = 'DEVICE_IFA'
    TIME_KEY: str = 'REQUEST_TIME'
    IP_KEY: str = 'DEVICE_IP'
    CITY_KEY: str = 'GEO_CURRENT_CITY'
    LANG_KEY: str = 'DEVICE_LANGUAGE'
    unused_columns: Tuple[str] = (
        'CUMNORM_23',
    )

    def __post_init__(self):
        self.USECOLS = [
            self.TIME_KEY, self.IP_KEY, self.PRIMARY_KEY, self.CITY_KEY, self.LANG_KEY
        ]
        self.unused_columns = list(self.unused_columns)


@dataclass
class AggTransforms:
    input_keys: InputKeys
    time_diff: List[str] = field(default_factory=lambda: ['mean', 'max', 'min', 'std'])
    ip: List[str] = field(default_factory=lambda: ['nunique'])
    city: List[str] = field(default_factory=lambda: ['nunique'])
    lang: List[str] = field(default_factory=lambda: ['nunique'])

    def __post_init__(self):
        self.transforms = {
            'TIME_DIFF': self.time_diff,
            self.input_keys.IP_KEY: self.ip,
            self.input_keys.CITY_KEY: self.city,
            self.input_keys.LANG_KEY: self.lang,
        }


def pickle_model_obj(obj, name):
    with open(MODELS_PATH / name, 'wb') as file:
        pickle.dump(obj, file)


def unpickle_model_obj(name):
    with open(MODELS_PATH / name, 'rb') as file:
        return pickle.load(file)


input_keys = InputKeys()
agg_trns = AggTransforms(input_keys=input_keys)
