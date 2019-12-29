FROM python:3.7

COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY credentials.yaml /

COPY . /
ADD db db

RUN python -m nltk.downloader punkt averaged_perceptron_tagger maxent_ne_chunker words
RUN python -m spacy download en

CMD ["python", "./grab_tweets.py"]
