FROM python:3.7-alpine

ADD grab_tweets.py /
ADD requirements.txt /

RUN pip install -r requirements.txt

CMD ["python", "./grab_tweets.py"]
