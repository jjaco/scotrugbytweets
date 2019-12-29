FROM python:3.7

COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY . /
ADD templates templates

CMD ["python", "./app.py"]

EXPOSE 8050
