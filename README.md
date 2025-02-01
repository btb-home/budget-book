# budget-book
BTB budget book project

# Docker 
docker build -t btbdocker/budget-book:0.0.1 -f docker/Dockerfile .
docker rm poc
docker run -p 80:8030 --name poc btbdocker/budget-book:0.0.1

