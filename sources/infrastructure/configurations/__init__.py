from os import getenv


EXEC_PROFILE = getenv("EXEC_PROFILE", "dev")

match EXEC_PROFILE.lower():
    case "dev":
        from .dev import Configuration
    case "prod":
        from .prod import Configuration
    case "local":
        from .local import Configuration  # noqa
    case _:
        raise RuntimeError("No suitable configuration found.")

configuration = Configuration.validate()

print(f'Profile set from "{EXEC_PROFILE.title()} Settings"')
