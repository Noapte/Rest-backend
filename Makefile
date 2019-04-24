build:
	docker-compose build

rebuild:
	@make clean_all
	@make build

run:
	docker-compose up -d

run_db:
	docker-compose up -d postgres 

stop:
	docker-compose stop

clean:
	docker-compose down -v

clean_image:
	docker rmi -f `docker images -a | grep documents | cut -d ' ' -f1`

clean_all:
	@make clean
	@make clean_image || true

logs:
	docker-compose logs -f

shell:
	docker-compose exec backend sh
