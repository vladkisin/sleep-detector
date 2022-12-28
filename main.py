import click
from src.common import unpickle_model_obj, InputKeys
from src.model import BotDetector


@click.group()
def cli():
    pass


@click.command()
def train():
    click.echo('PASS')


@click.command()
@click.option('--file_name', required=True, type=str, help='Name of the file in the data folder')
@click.option('--primary_key', default='DEVICE_IFA', help='Column name of the unique id')
@click.option('--time_key', default='REQUEST_TIME', help='Column name of the request time')
@click.option('--ip_key', default='DEVICE_IP', help='Column name of the device IP address')
@click.option('--city_key', default='GEO_CURRENT_CITY', help='Column name of the current city')
@click.option('--lang_key', default='DEVICE_LANGUAGE', help='Column name of the device language')
def predict(file_name, primary_key,
            time_key, ip_key,
            city_key, lang_key):
    preprocessor = unpickle_model_obj('preprocessor.pkl')
    clf = unpickle_model_obj('forest.pkl')
    input_keys = InputKeys(
        PRIMARY_KEY=primary_key,
        TIME_KEY=time_key,
        IP_KEY=ip_key,
        CITY_KEY=city_key,
        LANG_KEY=lang_key,
    )
    detector = BotDetector(
        preprocessor=preprocessor, clf=clf, input_keys=input_keys
    )
    detector.predict(
        file_path=file_name, save_to_disk=True
    )


if __name__ == '__main__':
    cli.add_command(train, 'train')
    cli.add_command(predict, 'predict')
    cli()

