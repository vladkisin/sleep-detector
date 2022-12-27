import numpy as np
from datetime import timedelta


def generate_fake_ip():
    return '.'.join(
        map(
            str, np.random.randint(0, 256, size=4)
        )
    )


def generate_mus_human():
    boundaries = [
        (2, 5),
        (5, 10),
        (10, 15),
        (15, 19),
        (19, 24)
    ]
    peaks = []
    for upper, lower in boundaries:
        peaks.append(np.random.rand() * (upper - lower) + lower)
    return peaks


def generate_mus_fake(num_peaks: int):
    peaks = []
    for _ in range(num_peaks):
        peaks.append(np.random.rand() * 23.9999)
    return peaks


def generate_hour_start():
    # Generate starting hour from shifted gamma distribution
    hour_started = np.random.gamma(shape=1, scale=2.5)
    hour_started = hour_started - 1.5 if hour_started >= 1.5 else hour_started + 22.5
    # Clip by maximum 24 hours
    hour_started = min(hour_started, 23.999)
    return hour_started


def generate_sleep_interval():
    # Generate num of hours slept from normal distribution with 8 on average
    hours_slept = np.random.normal(loc=8, scale=1)
    # Take starting hour and calculate ending hour
    hour_start = generate_hour_start()
    hour_end = (hour_start + hours_slept) % 24
    return hour_start, hour_end


def zero_sleep(distribution: np.array, hour_start: int, hour_end: int):
    hour_start = int(np.round(hour_start))
    hour_end = int(np.round(hour_end))
    if hour_end < hour_start:
        hour_end += 24
    zero_ind = list(
        map(lambda x: x % 24, range(hour_start, hour_end))
    )
    distribution[zero_ind] = 0
    return distribution


def softmax(arr: np.array, softmax_temperature: float):
    return np.exp(arr/softmax_temperature) / np.sum(np.exp(arr/softmax_temperature))


def normalize_vector(vec: np.array):
    return vec / np.linalg.norm(vec)


def generate_human_distribution(sigma=1.25, size=500, softmax_temperature=0.3):
    # Generate distribution entries
    X = np.concatenate(
        [np.random.normal(mu, sigma, size) for mu in generate_mus_human()]
    ).clip(0, 24)
    # Generate histogram and normalize it by max value
    hist = np.histogram(X, np.arange(0, 25))[0]
    hist = hist / hist.max()
    # Apply softmax
    hist_softmax = softmax(hist, softmax_temperature)
    # Apply sleeping mask
    hour_start, hour_end = generate_sleep_interval()
    return zero_sleep(hist_softmax, hour_start, hour_end)


def generate_fake_distribution(sigma=1.75, size=500, softmax_temperature=0.3):
    # Generate number of peaks:
    n_peaks = np.random.randint(1, 24)
    # Generate distribution entries
    X = np.concatenate([np.random.normal(mu, sigma, size) for mu in generate_mus_fake(n_peaks)]).clip(0, 24)
    # Generate histogram and normalize it by max value
    hist = np.histogram(X, np.arange(0, 25))[0]
    hist = hist / hist.max()
    # Apply softmax
    hist_softmax = softmax(hist, softmax_temperature)
    return hist_softmax


def random_date_in_interval(start, interval=3600):
    return start + timedelta(seconds=np.random.random() * interval)


def generate_n_dates_equal(start_date, n_dates):
    delta = 3600 / max(n_dates - 1, 1)
    dates = [start_date]
    i = 1
    while i < n_dates:
        dates.append(dates[-1] + timedelta(seconds=delta+np.random.normal()*3))
        i += 1
    return dates


def random_cutoff(records):
    if len(records) == 0:
        return records
    if np.random.random() > 0.8:
        dat = np.random.randint(0, len(records), size=2)
        a, b = min(dat), max(dat)
    else:
        a, b = 0, len(records)
    return records[a:b]


def generate_fake_hour(n_entries, equal_range, ddos, base_date, ips, ifa, langs, cities):
    if equal_range:
        n_entries = int(n_entries)
        dates = generate_n_dates_equal(base_date, n_entries)
        return random_cutoff(
            list(
                zip(
                    dates, np.random.choice(ips, n_entries), [ifa] * n_entries,
                    np.random.choice(cities, size=n_entries), np.random.choice(langs, size=n_entries),
                    [1] * n_entries  # Fake flag
                )
            )
        )
    elif ddos:
        records = []
        base_date = base_date + timedelta(seconds=np.random.random() * 55 * 60)
        interval = np.random.random() * 3 * 60
        for _ in range(int(n_entries)):
            records.append(
                (random_date_in_interval(base_date, interval=interval), np.random.choice(ips),
                 ifa, np.random.choice(cities), np.random.choice(langs), 1)
            )
        return random_cutoff(records)
    else:
        records = []
        for _ in range(int(n_entries)):
            records.append(
                (random_date_in_interval(base_date), np.random.choice(ips),
                 ifa, np.random.choice(cities), np.random.choice(langs), 1)
            )
        return random_cutoff(records)
