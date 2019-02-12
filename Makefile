build:
	docker-compose build app
run:
	docker-compose run --rm --service-ports app flask run -h 0.0.0.0 -p 80
test:
	docker-compose run --rm app pytest tests
test-debug:
	docker-compose run --rm app pytest tests -s --lf
flake8:
	docker-compose run --rm app flake8 .
