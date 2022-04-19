# Airflow Service

## Requirements

* Python 3.9.7 (https://www.python.org/)
* Python Version Management: pyenv (https://github.com/pyenv/pyenv)


## Development configuration (on Mac M1)

### Install
* Install pyenv
```shell
brew update
# [if zlib is not installed yet]
# brew install zlib
# don't miss set up the environment variables in your shell profile
brew install pyenv
brew upgrade pyenv
pyenv init
# don't miss source shell rc
```

* Install Python 3.9.7
```shell
pyenv install 3.9.7
# [optional]
# pyenv global 3.9.7
```

* Create the environment, go to the project root and run:
```shell
pyenv local 3.9.7
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install psycopg2-binary --force-reinstall --no-cache-dir
pip install -r requirements-dev.txt
pip install -r requirements.txt
```

* Install pre-commit
```shell
pre-commit install
```


### Run

#### In Development

1. Configure environment variables. Copy `.env.example` to `.env` and set/change the values accordingly.

2. Create the necessary files and directories. Run: `mkdir ./logs`

3. Start PostgreSQL
```shell
docker-compose up postgres
```

4. Create database and schema:
```postgresql
CREATE DATABASE <database_name>;
-- now, change to <database_name> database and create schema airflow
CREATE SCHEMA airflow;
```

5. Run Redis
```shell
docker-compose up redis
```

6. Run Airflow database migrations and create the first user account
```shell
docker-compose up airflow-init
```

7. Run Airflow webserver
```shell
docker-compose up airflow-webserver
```

8. Run Airflow scheduler
```shell
docker-compose up airflow-scheduler
```

9. Run Airflow worker
```shell
docker-compose up airflow-worker
```

## Additional configuration:

To create separate users in order to store airflow related tables in one schema and application tables in another:

```postgresql
CREATE USER airflow WITH ENCRYPTED PASSWORD 'somepass';
ALTER SCHEMA airflow OWNER TO airflow;
ALTER ROLE airflow SET search_path = airflow,public;

GRANT ALL PRIVILEGES ON DATABASE expos_service TO airflow;

-- if you get 'no schema selected' errors, issue the following 2 commands
GRANT USAGE, CREATE ON SCHEMA airflow TO airflow, public;
-- if you get permission denied to create extension you might need to grant superuser too
-- this depends on postgres version. As of v13 some extensions are considered safe
-- to create from users with CREATE privileges on current DB
-- https://stackoverflow.com/a/63781812/10533611
-- https://www.postgresql.org/docs/13/contrib.html
```

Application layer should do the same procedure with a different user to interact with `public` schema
