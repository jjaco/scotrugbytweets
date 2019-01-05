FROM python:3.7

ADD grab_tweets.py /
ADD requirements.txt /

RUN pip3 install -r requirements.txt

CMD ["python", "./grab_tweets.py"]
