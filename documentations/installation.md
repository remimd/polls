# Installation

## Dependencies

### Required

* **Python 3.10**
* [**Poetry**](https://github.com/python-poetry/poetry)
* **PostgreSQL**

## Installation

### Python dependencies

```bash
poetry install
```

***Basic usage of Poetry***

* *Start shell environment:*

```bash
poetry shell
```

## Configuration

### .env

Create `.env` file at the root of the project:

```dotenv
SECRET_KEY=<YOUR_SECRET_KEY>

DB_NAME=<YOUR_DATABASE_NAME>
DB_USER=<YOUR_DATABASE_USER>
DB_PASSWORD=<YOUR_DATABASE_PASSWORD>
DB_HOST=<YOUR_DATABASE_HOST>
DB_PORT=<YOUR_DATABASE_PORT>
```

### Initialize Database

*Reset database and apply migrations.*

```bash
python manage.py init_bdd
```

### Local settings

To override the development settings, you can create `local.py` file in `sources/infrastructure/configurations` folder:

```python
from .dev import Configuration as DevelopmentConfiguration


class Configuration(DevelopmentConfiguration):
    """ Your configuration here """
```

*To use these settings, you must add this environment variable: `EXEC_PROFILE=local`.*
