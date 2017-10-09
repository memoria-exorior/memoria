
export PYTHONPATH=.:$$PYTHONPATH

# -------------------------------------------------------------------------------------------------
# dev mongo db provisioning 

dev-docker-mongo-start:
	docker run -p 27017:27017 --name dev-memoria-mongo -d mongo

dev-docker-mongo-stop:
	docker rm -f dev-memoria-mongo

dev-docker-mongo-shell:
	docker exec -it dev-memoria-mongo mongo
	
dev-mongo-shell:
	mongo localhost

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

