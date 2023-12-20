# python-docker-boilerplate

Boilerplate code for starting a Python project with Docker

## Set up

Clone the repo

```
git clone [copy from above]
cd [directory from above]
```

copy .env-example to .env

```
cp .env-example .env
```

edit .env with actual environment variables

build container
```
docker-compose build
```

start container
```
docker-compose up -d
```

## Run the program

```
docker-compose run --rm app python [etc.]
```
