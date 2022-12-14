# Configurations

## Table of contents

1. [Requirements](#requirements)
2. [Dependencies](#dependencies)
3. [Installation](#installation)
4. [How to use](#how-to-use)
5. [Docker](#docker)
6. [Logger](#logger)

## Requirements

- [Python](https://www.python.org/) (version >= [3.8.10](https://www.python.org/downloads/release/python-3810/))
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [MySQL](https://www.mysql.com/) (version >= 8.0.28) ([MariaDB](https://mariadb.org/))

## Dependencies

On Ubuntu

```bash
$ sudo apt install python3-dev libmysqlclient-dev apache2 apache2-dev make libapache2-mod-wsgi-py3
```

## Linux Environment Variables

Variables used for the Project:

- MYSQL_DATABASE=STRING
- MYSQL_HOST=STRING
- MYSQL_PASSWORD=STRING
- MYSQL_USER=STRING
- HOST=STRING
- PORT=STRING
- ORIGINS=ARRAY
- SSL_SERVER_NAME=STRING
- SSL_PORT=STRING
- SSL_CERTIFICATE=PATH
- SSL_KEY=PATH
- SSL_PEM=PATH
- OPENAPI_HOST=STRING
- OPENAPI_PORT=STRING
- OPENAPI_VERSION=STRING
- ID=STRING
- KEY=STRING

## Installation

### Pip

```bash
$ python3 -m venv venv
$ . venv/bin/activate
$ pip install -r requirements.txt
```

## How to use

### Start API

**Python**

```bash
$ MYSQL_DATABASE= \
  MYSQL_HOST= \
  MYSQL_PASSWORD= \
  MYSQL_USER= \
  HOST= \
  PORT= \
  ORIGINS = \
  SSL_SERVER_NAME= \
  SSL_PORT= \
  SSL_CERTIFICATE= \
  SSL_KEY= \
  SSL_PEM= \
  OPENAPI_HOST= \
  OPENAPI_PORT= \
  OPENAPI_VERSION= \
  ID= \
  KEY= \
  MODE=production \
  python3 server.py
```

**MOD_WSGI**

```bash
$ MYSQL_DATABASE= \
  MYSQL_HOST= \
  MYSQL_PASSWORD= \
  MYSQL_USER= \
  HOST= \
  PORT= \
  ORIGINS= \
  SSL_SERVER_NAME= \
  SSL_PORT= \
  SSL_CERTIFICATE= \
  SSL_KEY= \
  SSL_PEM= \
  OPENAPI_HOST= \
  OPENAPI_PORT= \
  OPENAPI_VERSION= \
  ID= \
  KEY= \
  MODE=production \
  mod_wsgi-express start-server wsgi_script.py \
  --user www-data \
  --group www-data \
  --port '${PORT}' \
  --ssl-certificate-file '${SSL_CERTIFICATE}' \
  --ssl-certificate-key-file '${SSL_KEY}' \
  --ssl-certificate-chain-file '${SSL_PEM}' \
  --https-only \
  --server-name '${SSL_SERVER_NAME}' \
  --https-port '${SSL_PORT}'
```

## Docker

### Build

Build smswithoutborders-dev-backend development docker image

```bash
$ docker build --target development -t smswithoutborders-dev-backend .
```

Build smswithoutborders-dev-backend production docker image

```bash
$ docker build --target production -t smswithoutborders-dev-backend .
```

### Run

Run smswithoutborders-dev-backend development docker image. Fill in all the neccessary [environment variables](#linux-environment-variables)

```bash
$ docker run -d -p 9000:9000 \
  --name smswithoutborders-dev-backend \
  --env 'MYSQL_DATABASE=' \
  --env 'MYSQL_HOST=' \
  --env 'MYSQL_PASSWORD=' \
  --env 'MYSQL_USER=' \
  --env 'HOST=' \
  --env 'PORT=' \
  --env 'ORIGINS=' \
  --env 'OPENAPI_HOST=' \
  --env 'OPENAPI_PORT=' \
  --env 'OPENAPI_VERSION=' \
  --env 'ID=' \
  --env 'KEY=' \
  smswithoutborders-dev-backend
```

Run smswithoutborders-dev-backend production docker image. Fill in all the neccessary [environment variables](#linux-environment-variables)

```bash
$ docker run -d -p 9000:9000 \
  --name smswithoutborders-dev-backend \
  --env 'MYSQL_DATABASE=' \
  --env 'MYSQL_HOST=' \
  --env 'MYSQL_PASSWORD=' \
  --env 'MYSQL_USER=' \
  --env 'HOST=' \
  --env 'PORT=' \
  --env 'ORIGINS=' \
  --env 'SSL_SERVER_NAME=' \
  --env 'SSL_PORT=' \
  --env 'SSL_CERTIFICATE=' \
  --env 'SSL_KEY=' \
  --env 'SSL_PEM=' \
  --env 'OPENAPI_HOST=' \
  --env 'OPENAPI_PORT=' \
  --env 'OPENAPI_VERSION=' \
  --env 'ID=' \
  --env 'KEY=' \
  smswithoutborders-dev-backend
```

> Read in a file of environment variables with `--env-file` command e.g. `docker run -d -p 9000:9000 --name smswithoutborders-dev-backend --env-file myenv.txt smswithoutborders-dev-backend`

> Mount path to SSL files with volume `-v` command e.g. `docker run -v /host/path/to/certs:/container/path/to/certs -d -p 9000:9000 --name smswithoutborders-dev-backend --env-file myenv.txt smswithoutborders-dev-backend`

## logger

### Python

```bash
$ python3 server.py --logs=debug
```

### Docker

Container logs

```bash
$ docker logs smswithoutborders-dev-backend
```

API logs in container

```bash
$ docker exec -it smswithoutborders-dev-backend tail -f <path_to_mod_wsgi_error_logs>
```
