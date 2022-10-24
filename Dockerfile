FROM python:3.10-slim

EXPOSE 80

WORKDIR /app

COPY ./ .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD [ "gunicorn", "--conf", "gunicorn-conf.py", "--bind", "0.0.0.0:80", "main:app" ]
