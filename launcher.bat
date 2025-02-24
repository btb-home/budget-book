@echo off
:: 변수 설정
set IMAGE_NAME=btbdocker/budget-book-be
set IMAGE_TAG=0.0.1
set CONTAINER_NAME=budget-book-be
set PORT=80
set CONTAINER_PORT=8030

:: Docker 이미지 빌드
docker build -t %IMAGE_NAME%:%IMAGE_TAG% -f docker/Dockerfile .

:: 실행 중인 컨테이너가 있다면 중지하고 삭제
docker stop %CONTAINER_NAME%
docker rm %CONTAINER_NAME%

:: 새 컨테이너 실행
docker run -d -p %PORT%:%CONTAINER_PORT% --name %CONTAINER_NAME% %IMAGE_NAME%:%IMAGE_TAG%

echo "Docker container %CONTAINER_NAME% is running on port %PORT%."
