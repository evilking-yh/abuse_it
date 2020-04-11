FROM python:3.7
LABEL maintainer="hulk"
ENV REFRESHED_AT 2018-12-20

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

ENV PROJECT_DIR=/app NODE_ENV=production APP_PORT=5000
WORKDIR $PROJECT_DIR
RUN mkdir -p $PROJECT_DIR
COPY app/ $PROJECT_DIR

EXPOSE $APP_PORT

CMD ["python", "flask_bin/app_start.py"]