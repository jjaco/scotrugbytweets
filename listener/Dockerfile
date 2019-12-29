FROM python:3.7

ADD grab_tweets.py /
ADD requirements.txt /
ADD nlp.py /
ADD db db
ADD credentials.yaml /

RUN pip3 install -r requirements.txt
RUN python -m nltk.downloader punkt averaged_perceptron_tagger maxent_ne_chunker words
RUN python -m spacy download en

CMD ["python", "./grab_tweets.py"]
