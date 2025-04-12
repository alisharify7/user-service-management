FROM docker.arvancloud.ir/python:3.13-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

COPY . /app/


RUN apk add curl

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
