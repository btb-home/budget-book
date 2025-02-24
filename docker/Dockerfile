FROM python:3.12.3

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY .env.dev /code/.env

# .env.dev 파일을 컨테이너로 복사
COPY ./conf/dev/ /code/conf/dev/

# 환경 변수 파일을 로드하는 방법은 애플리케이션에서 다르게 설정해야 할 수 있음
ENV ENV_PATH="/code/conf/dev/.env.dev"
ENV APP_ENVIRONMENT=dev

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8030"]