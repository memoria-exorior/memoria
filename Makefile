
export PYTHONPATH=.:$$PYTHONPATH

# -------------------------------------------------------------------------------------------------
# docker

docker-build:
	docker build -t memoria-service .

docker-deploy: docker-build
	docker run -p 27017:27017 --name memoria-mongodb -d mongo
	docker run -d \
		-e MONGO_HOST=mongodb \
		-p 8888:8888 \
		--link memoria-mongodb:mongodb \
		--name memoria-service \
		memoria-service

docker-undeploy:
	docker rm -f memoria-mongodb
	docker rm -f memoria-service

docker-mongo-deploy:
	docker run -p 27017:27017 --name memoria-mongodb -d mongo

docker-mongo-undeploy:
	docker rm -f memoria-mongodb

docker-mongo:
	docker exec -it memoria-mongo mongo

# -------------------------------------------------------------------------------------------------
# linting

lint: lint-flake8

lint-pep8:
	venv/bin/pep8 memoria

lint-pylint:
	find memoria -name *.py | xargs venv/bin/pylint -rn -f colorized

lint-flake8:
	venv/bin/flake8 memoria

# -------------------------------------------------------------------------------------------------
# tests

itest:
	find memoria -name *_itest.py | xargs venv/bin/python3 -m unittest

# -------------------------------------------------------------------------------------------------
# dev mode server

run:
	venv/bin/python3 memoria/app.py


# -------------------------------------------------------------------------------------------------
# other

deps-freeze:
	pip3 freeze > requirements.txt

clean:
	find memoria -name __pycache__ | xargs rm -f
