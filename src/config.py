import pathlib


def get_root():
    return pathlib.Path('.').resolve()


ROOT_PATH = get_root()
DATA_PATH = ROOT_PATH / 'data'
MODELS_PATH = ROOT_PATH / 'models'
SRC_PATH = ROOT_PATH / 'src'


lang_space = [
    'he', 'en', 'ru', 'ar', 'fr', 'es', 'tr'
]
lang_p = [
    0.65, 0.16, 0.08, 0.07, 0.02, 0.01, 0.01
]
city_space = [
    'Tel Aviv', 'Holon', 'Petah Tiqwa', 'Givatayim', 'Hod HaSharon',
    'Bat Yam', 'Haifa', 'Rishon LeZiyyon', 'Ramat Gan', 'Tiberias', 'Ramla',
    'Herzliya', 'Rehovot', 'Daliyat al Karmel', 'Bnei Brak', 'Nazareth',
    "Karmi'el", 'Qiryat Yam', 'Netanya', 'Eilat', 'Kfar Saba', 'Nehalim',
    'Ashdod', 'Rosh Ha‘Ayin', 'Lod', 'Elyakhin', 'Bet Dagan',
    'Yehud-Monosson', 'Kfar Yasif', 'West Jerusalem', 'Even Yehuda',
    'maalot Tarshiha', 'Jerusalem', "Modi'in Makkabbim Re'ut", 'Beersheba',
    'Bayt Iksa'
]
city_p = [
    0.366, 0.162, 0.116, 0.114, 0.038, 0.032, 0.032, 0.026, 0.024,
    0.008, 0.006, 0.006, 0.006, 0.004, 0.004, 0.004, 0.004, 0.004,
    0.004, 0.004, 0.004, 0.004, 0.002, 0.002, 0.002, 0.002, 0.002,
    0.002, 0.002, 0.002, 0.002, 0.002, 0.002, 0.002, 0.002, 0.002
]