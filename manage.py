import sys

from sources.infrastructure.server import Server
from sources.infrastructure.setup import setup_project


setup_project()

server = Server()


def main():
    from django.core.management import execute_from_command_line

    execute_from_command_line(argv=sys.argv)


if __name__ == "__main__":
    main()
