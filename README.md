# budget-book
BTB budget book project

# Docker 
docker build -t budget-book:0.0.1 -f docker/Dockerfile .
docker run -p 8030:8030 --name poc budget-book:0.0.1
