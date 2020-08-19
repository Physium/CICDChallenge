FROM python:3.8.5-alpine
WORKDIR /code
ENV FLASK_APP main.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 8000
ENV REDIS_SERVICE redis
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["flask", "run"]