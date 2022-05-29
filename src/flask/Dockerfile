FROM python:3.9

WORKDIR /website

COPY . .
COPY ssh /root/.ssh

RUN apt-get update && apt-get install ssh git python3-pip -y && \
    pip install --upgrade pip && \ 
    pip install -r requirements.txt && \
    chmod +x update.sh && \
    chmod 600 /root/.ssh/id_rsa && \
    mv update.sh app

WORKDIR /website/app
 
CMD sh update.sh && python3 app.py
