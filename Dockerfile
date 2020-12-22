FROM python:3.9-alpine

WORKDIR /app
RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY /app .

CMD ["python", "main.py"]