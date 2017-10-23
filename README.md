# Fact Service

A small service to manage a set of facts.

---

## Initialise Virtual Environment

```
python3.6 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:.
```

---

## Run Development Mode

### Containerised mongo with localhost memoria-service

```
make docker-build
make docker-mongo-deploy
make run
...
make docker-mongo-undeploy
```

### Containerised mongo and memoria-service

```
make docker-build
make docker-deploy
...
make docker-undeploy
```

### Containerised mongo and memoria-service (docker-compose)

```
make docker-build
docker-compose up
...
docker-compose down
```

---

## Run Tests

```
make itest
```

---

## Clean-up

```
make dev-docker-mongo-stop
```