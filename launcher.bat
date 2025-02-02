alembic revision --autogenerate
alembic upgrade head

docker build -t btbdocker/budget-book:0.0.1 -f docker/Dockerfile .
docker stop poc
docker rm poc
docker run -d -p 80:8030 --name poc btbdocker/budget-book:0.0.1
