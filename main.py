import logging
import warnings
import click
from src.config import DATA_PATH, city_space, city_p, lang_space, lang_p
from src.common import unpickle_model_obj, InputKeys, input_keys
from src.model import BotDetector
from src.generate.generators import generate_dataset, generate_ip_space

warnings.filterwarnings("ignore")
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)


@click.group()
def cli():
    pass


@click.command(help='Generates data for model testing')
@click.option('--n_users', required=True, type=int, help='Number of unique users in the data')
@click.option('--file_name', required=True, type=str,
              help='Name of the file in the data folder to write results')
def generate_test_data(n_users, file_name):
    ip_space = generate_ip_space(100)
    test_data = generate_dataset(n_users, ip_space, lang_space, lang_p, city_space, city_p, input_keys)
    test_data.to_csv(DATA_PATH / file_name, index=False)
    logger.info(f'Done! Saved to {DATA_PATH}')


@click.command(help='Runs trained model against provided input data')
@click.option('--file_name', required=True, type=str, help='Name of the file in the data folder')
@click.option('--primary_key', default='DEVICE_IFA',
              help='Column name of the unique id; default=DEVICE_IFA')
@click.option('--time_key', default='REQUEST_TIME',
              help='Column name of the request time; default=REQUEST_TIME')
@click.option('--ip_key', default='DEVICE_IP',
              help='Column name of the device IP address; default=DEVICE_IP')
@click.option('--city_key', default='GEO_CURRENT_CITY',
              help='Column name of the current city; default=GEO_CURRENT_CITY')
@click.option('--lang_key', default='DEVICE_LANGUAGE',
              help='Column name of the device language; default=DEVICE_LANGUAGE')
def predict(file_name, primary_key,
            time_key, ip_key,
            city_key, lang_key):
    preprocessor = unpickle_model_obj('preprocessor.pkl')
    clf = unpickle_model_obj('forest.pkl')
    new_input_keys = InputKeys(
        PRIMARY_KEY=primary_key,
        TIME_KEY=time_key,
        IP_KEY=ip_key,
        CITY_KEY=city_key,
        LANG_KEY=lang_key,
    )
    detector = BotDetector(
        preprocessor=preprocessor, clf=clf, input_keys=new_input_keys
    )
    detector.predict(
        file_path=file_name, save_to_disk=True
    )
    logger.info('Done!')


if __name__ == '__main__':
    cli.add_command(generate_test_data, 'generate_test_data')
    cli.add_command(predict, 'predict')
    cli()
