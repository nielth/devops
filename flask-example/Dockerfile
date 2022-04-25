FROM python:alpine3.15

WORKDIR /website

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "app.py" ] 