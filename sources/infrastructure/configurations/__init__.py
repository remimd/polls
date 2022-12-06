import logging
from os import getenv

from dotenv import load_dotenv


load_dotenv()

EXEC_PROFILE = getenv("EXEC_PROFILE", "dev")

match EXEC_PROFILE.lower():
    case "dev":
        from .dev import Configuration  # noqa
    case "prod":
        from .prod import Configuration  # noqa
    case "local":
        from .local import Configuration  # noqa
    case _:
        raise RuntimeError("No suitable configuration found.")

configuration = Configuration.verify()

_logger = logging.getLogger("configuration")
_logger.warning(f'Profile set from "{EXEC_PROFILE.title()} Configuration"')
