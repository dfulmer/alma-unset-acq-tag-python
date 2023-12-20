# Python Alma Unset Acq Tags

Alma Unset Acq Tags in Python.

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

This command will run the create-sets.py script, which combines two sets into an Itemized set:

```
docker-compose run --rm app python create-sets.py
```

This command will run the change-tags.py script, which will change the Management Tags of the newly created set to "Don't Publish":

```
docker-compose run --rm app python change-tags.py
```
