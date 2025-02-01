FROM python:3.12.3

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY .env.dev /code/.env

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8030"]