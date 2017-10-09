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

```
make dev-docker-mongo-start
make run
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