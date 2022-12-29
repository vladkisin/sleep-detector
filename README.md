# Bot sleep detector project

## General description
The repository provides a small project which entails data generation, exploration, feature engineering, ML model training and inference.
The task being solved - to identify bot accounts in the adtech data stream. 
To achieve the goal daily aggregated time-based features are used along with some other. 

Important note: the data are generated in such a way that one unique user can appear in one date only. 
However, random crops during the day are implemented.
In real-world scenario we would use a more complicated rolling window statistics.

### Feature space
- *`X`* (X - int): Features representing total count of requests at hour X for a user.
- *ZERO_ACTIVE_HOURS*: The number of hour periods where activity is none, max 24.
- *TOTAL_REQS*: Total number of daily requests by a user.
- *NORM_`X`*(X - int): Features representing normalized total count of requests at hour X for a user.
- *CUMNORM_`X`*(X - int): Features representing sum normalized total count of requests from 0 up to hour X for a user.
- *NORM_MAX_PEAK*: Max normalized num of requests for a user.
- *NORM_HOURS_STD*: Standard deviation for normalized hourly requests for a user.
- *(TIME_DIFF, mean)*: Average difference between consecutive requests in seconds.      
- *(TIME_DIFF, max)*: Maximal difference between consecutive requests in seconds.
- *(TIME_DIFF, min)*: Minimal difference between consecutive requests in seconds.           
- *(TIME_DIFF, std)*: Standard deviation of difference between consecutive requests in seconds.
- *(DEVICE_IP, nunique)*: Number of unique IPs that device sent requests from for a user.
- *(GEO_CURRENT_CITY, nunique)*: Number of unique cities that device sent requests from for a user.
- *(DEVICE_LANGUAGE, nunique)*: Number of unique device languages that device sent requests from for a user.


## Experiments
Short experiments can be found in the form of jupyter noteboks in `jnb` folder.
There are two notebooks: one for data generation routines and one for exploration and modelling routines.

## Environment
This repository along with [docker repository](https://hub.docker.com/r/uladzislaukisin/sleepdetect) provide code and trained model artifacts to run the model against input data.
For everything to work properly one should strictly follow the specifications of the API.

To reproduce the environment, a recommended way is to use the docker image.

### Option 1: Reach out the CLI with Docker image:
The following set of commands should be performed in a folder that one wants to provide input data and store the results in (it would be mounted as volume to the container).
On Windows one should run `wsl` command before executing the rest. [In case WSL and Linux on Windows is not installed](https://learn.microsoft.com/en-us/windows/wsl/install).
```console
docker pull uladzislaukisin/sleepdetect:latest  # Pull the image from docker hub
docker run -dit --name sleepdetect -v $(pwd):/app/data uladzislaukisin/sleepdetect:latest  # Run the container in detach mode and mount current dir as volume to app/data
docker exec -it sleepdetect sh  # Enter the terminal in the container
```
### Option 2: Make local Python environment
If Docker doesn't work for you for some reason, you can try to install Python environment locally.
To build local Python environment pull the git repository and install Python environment either with [conda](https://docs.conda.io/en/latest/miniconda.html) with `environent.yml` in the `env` folder or via pip (`pip install -r requirements.txt`).
Then, CLI commands should be run in the terminal from the root folder of the repository.

## CLI API
The API interface is reached via main.py module.

The list of methods and references are available with `--help` argument. 
```console
python main.py --help
```
Output
```console
Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  generate_test_data  Generates data for model testing
  predict             Runs trained model against provided input data
```

The API can either generate synthetic data in the same fashion that it was made for model development or make prediction on provided data.

### Generate data
```console
python main.py generate_test_data --help
```
Output:
```console
Usage: main.py generate_test_data [OPTIONS]

  Generates data for model testing

Options:
  --n_users INTEGER  Number of unique users in the data  [required]
  --file_name TEXT   Name of the file in the data folder to write results
                     [required]
  --help             Show this message and exit.
```

To generate the data one should provide the number of users to be generated and the file name. The data would be stored to the mounted data point in case of docker container or in `data/` folder in case of local environment.

**Example:**
```console
python main.py generate_test_data --n_users 10 --file_name test_data.csv
```
Output
```console
2022-12-29 13:13:54,934 Done! Saved to /app/data
```

### Make predictions
```console
python main.py predict --help
```
Output:
```console
Usage: main.py predict [OPTIONS]

  Runs trained model against provided input data

Options:
  --file_name TEXT    Name of the file in the data folder  [required]
  --primary_key TEXT  Column name of the unique id; default=DEVICE_IFA
  --time_key TEXT     Column name of the request time; default=REQUEST_TIME
  --ip_key TEXT       Column name of the device IP address; default=DEVICE_IP
  --city_key TEXT     Column name of the current city;
                      default=GEO_CURRENT_CITY
  --lang_key TEXT     Column name of the device language;
                      default=DEVICE_LANGUAGE
  --help              Show this message and exit.
```
This method runs the trained model against provided input data. 

**IMPORTANT:** the data provided should be in csv format, with `,` as separators and no compression. It's highly important that the schema of the data holds: the API expects the file to contain a list of columns described above (with default names or specified in the parameters otherwise).

**Example:**
```console
python main.py predict --file_name test_data.csv
```
Output
```console
2022-12-29 13:19:26,438 Done!
```
The data folder now contains one more file called `test_data_result.csv` (_result is added to original file name), where the are unique user IDs with predictions whether the user is considered as bot or not based on timely activity, IP, city and device language patterns.
