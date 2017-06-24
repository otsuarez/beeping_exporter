all: help

new: build run
	
help:
	@echo ""
	@echo "make build # build image"
	@echo "make run # run container"
	@echo "make [start|stop] # [start|stop] container"
	@echo "make clean # stop and remove container"
	@echo "make sh # launch a shell running inside the container"
	@echo "make logs # view container logs"

start:
	docker start beeping_exporter

stop:
	docker stop beeping_exporter

clean:
	docker stop beeping_exporter ; docker rm beeping_exporter

build:
	docker build -t otsuarez/beeping_exporter:latest .
	
run:
	files/update_beeping_env.sh
	docker run -d -p 9118:9118 -p 8080:8080 --env-file beeping_exporter.env --name beeping_exporter otsuarez/beeping_exporter:latest
	
sh:
	docker exec -it beeping_exporter bash


logs:
	docker logs -f --tail 10 beeping_exporter	
