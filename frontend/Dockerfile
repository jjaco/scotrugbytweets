FROM python:3.7

ADD app.py /
ADD templates templates
ADD requirements.txt /

RUN pip3 install -r requirements.txt

CMD ["python", "./app.py"]

EXPOSE 5000
