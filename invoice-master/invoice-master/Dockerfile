FROM python:alpine3.7
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/

RUN pip3 install --upgrade pip

RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers  cairo pango jpeg-dev libffi-dev musl-dev zlib-dev gcc glib msttcorefonts-installer ca-certificates \
    && update-ms-fonts  fc-cache -f \
    && python3 -m pip install -r requirements.txt --no-cache-dir



COPY . /code/
RUN python3 manage.py migrate

RUN python3 manage.py collectstatic --no-input --clear

