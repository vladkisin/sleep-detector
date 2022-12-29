FROM python:3.9

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip3 install -r requirements.txt

COPY models ./models
COPY src ./src
COPY main.py ./main.py
