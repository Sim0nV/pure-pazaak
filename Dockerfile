FROM python:3.9.5
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
RUN apt-get -y update
# RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
COPY . /bot
CMD python main.py