FROM python:3.9.5
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get -y update && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY . /bot
CMD python main.py
