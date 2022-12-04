import sys

from sources.infrastructure.server import Server
from sources.infrastructure.setup import setup_project


def main():
    setup_project()

    from django.core.management import execute_from_command_line

    execute_from_command_line(argv=sys.argv)


server = Server()

if __name__ == "__main__":
    main()
