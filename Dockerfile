FROM python:3.7.0

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN set -ex && mkdir /app

WORKDIR /app

RUN python -m pip install pip --upgrade && pip install pipenv

COPY . .

RUN set -ex && pipenv install --deploy --system

EXPOSE 8000

CMD ["python3", "app.py"]
