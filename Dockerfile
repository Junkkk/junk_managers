FROM python:3.9-alpine

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

COPY . /usr/src/junk_managers
WORKDIR /usr/src/junk_managers
RUN pip install -r requirements.txt
#RUN alembic upgrade head

#EXPOSE 8000
CMD ["python", "app/main.py"]