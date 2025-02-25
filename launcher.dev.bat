@echo off
:: 변수 설정
set IMAGE_NAME=btbdocker/budget-book-be
set IMAGE_TAG=0.0.1
set CONTAINER_NAME=budget-book-be
set REDIS_CONTAINER_NAME=budget-book-be-redis
set APP_CONTAINER_NAME=budget-book-be-app
set PORT=80
set CONTAINER_PORT=8030

:: 실행 중인 기존 컨테이너가 있으면 중지하고 삭제
echo Stopping and removing existing containers...
docker stop %REDIS_CONTAINER_NAME% %APP_CONTAINER_NAME%
docker rm %REDIS_CONTAINER_NAME% %APP_CONTAINER_NAME%

:: Docker Compose로 빌드하고 실행
echo Building and running containers with Docker Compose...
docker-compose up --build -d

:: 실행 결과 출력
if %ERRORLEVEL%==0 (
    echo Docker containers are running.
) else (
    echo Failed to start Docker containers.
)
