import pathlib

def get_root():
    return pathlib.Path('.').resolve().parents[0]


ROOT_PATH = get_root()
DATA_PATH = ROOT_PATH / 'data'
SRC_PATH = ROOT_PATH / 'src'
USECOLS = [
    'REQUEST_TIME', 'DEVICE_IP', 'DEVICE_IFA', 'GEO_CURRENT_CITY', 'DEVICE_LANGUAGE'
]
PRIMARY_KEY = 'DEVICE_IFA'
