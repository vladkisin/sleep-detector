import uuid
from datetime import datetime
from src.generate.helpers import *


def generate_ip_space(num_ips: int):
    ips = set()
    for _ in range(num_ips):
        ips.add(generate_fake_ip())
    return list(ips)


def generate_hourly_distribution(fake: bool):
    if fake:
        res = generate_fake_distribution()
    else:
        res = generate_human_distribution()
    return normalize_vector(res)


def generate_human_entries(ip_space, lang_space, lang_p, city_space, city_p):
    # Distribution
    dist = generate_hourly_distribution(fake=False)
    dist = np.round(dist * np.random.normal(loc=15, scale=3))

    # Generating records
    ifa = str(uuid.uuid4())  # Make up IFA
    ips = np.random.choice(ip_space, size=np.random.randint(1, 4))  # Choose a number of IPs
    lang = np.random.choice(lang_space, p=lang_p)
    city = np.random.choice(city_space, p=city_p)
    records = []
    base_num_day = np.random.randint(19, 26)
    for start in range(len(dist)):
        n_entries = dist[start]
        base_date = datetime(2022, 12, base_num_day, start, 0)  # Day in December 2022
        for _ in range(int(n_entries)):
            records.append(
                (random_date_in_interval(base_date), np.random.choice(ips), ifa, lang, city)
            )
    return records


def generate_bot_entries(ip_space, lang_space, lang_p, city_space, city_p):
    dist = generate_hourly_distribution(fake=True)
    dist = np.round(dist * np.random.uniform(20, 120))
    ifa = str(uuid.uuid4())  # Make up IFA
    ips = np.random.choice(ip_space, size=np.random.randint(1, 5))  # Choose a number of IPs
    langs = np.random.choice(lang_space, p=lang_p, size=np.random.choice(range(1, 4), p=[0.8, 0.15, 0.05]))
    cities = np.random.choice(city_space, p=city_p, size=np.random.choice(range(1, 4), p=[0.8, 0.15, 0.05]))
    records = []
    base_num_day = np.random.randint(19, 26)

    sd = np.random.random()
    if sd > 0.9:
        equal_range, ddos = True, False
    elif sd < 0.1:
        equal_range, ddos = False, True
    else:
        equal_range, ddos = False, False

    for start in range(len(dist)):
        n_entries = dist[start]
        base_date = datetime(2022, 12, base_num_day, start, 0)  # Day in December 2022
        records.extend(generate_fake_hour(n_entries, equal_range, ddos, base_date, ips, ifa, langs, cities))
    return records
