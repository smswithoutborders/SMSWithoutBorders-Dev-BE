# Configurations

## Table of contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Setup](#setup)

## Requirements

- [MySQL](https://www.mysql.com/) (version >= 8.0.28) ([MariaDB](https://mariadb.org/))
- [Python](https://www.python.org/) (version >= [3.8.10](https://www.python.org/downloads/release/python-3810/))
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## Dependencies

On Ubuntu **libmysqlclient-dev** is required

```
sudo apt install python3-dev libmysqlclient-dev
```

## Installation

Create a Virtual Environments **(venv)**

```
python3 -m venv venv
```

Move into Virtual Environments workspace

```
. venv/bin/activate
```

Install all python packages

```
python -m pip install -r requirements.txt
```

## Setup

All configuration files are found in the **[.config](../.config)** directory.

### Development configurations

**[default.ini](../.config/example.default.ini)** is the default configuration file.

To set up Database and API, copy the template files "example.default.ini" and rename to "default.ini"

```
cp .config/example.default.ini .config/default.ini
```

### Access configurations

**[setup.ini](../.config/example.setup.ini)** is the access configuration file.

To set up access, copy the template files "example.setup.ini" and rename to "setup.ini"

```
cp .config/example.setup.ini .config/setup.ini
```

### Products configurations

**[products.ini](../.config/example.products.ini)** is the products configuration file.

To set up products, copy the template files "example.products.ini" and rename to "products.ini"

```
cp .config/example.products.ini .config/products.ini
```

### Add Products to database

New products are fetched from the product **[info.json](../products/info.json)** file and added to the database the first time the server starts. Each product is an object in the **[info.json](../products/info.json)** file and it's metadata contains:

- name = The name of the Product
- label = The Display name for the Product
- description = The Product's description
- documentation = The Product's documentation

## How to use

### Start API

```bash
python3 server.py
```

## API SandBox

```
<host>:<PORT>/<VERSION>/api-docs/
```
