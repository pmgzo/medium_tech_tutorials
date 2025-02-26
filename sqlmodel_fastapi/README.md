# Run application

## To start database

```bash
docker run --name postgres-demo -e POSTGRES_PASSWORD=mysecretpassword -p 5432:5432 -d postgres
```

## Add Data into the database

```bash
python main.py
```

## To run API

```bash
fastapi dev main.py
```
