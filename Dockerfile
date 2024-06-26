FROM python:3.11

RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./src ./src

CMD ["python3", "src/main.py", "run"]