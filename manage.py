import sys

from sources.infrastructure.setup import setup_project


def main():
    from django.core.management import execute_from_command_line

    execute_from_command_line(argv=sys.argv)


def create_server():
    from sources.infrastructure.blacksheep.application import Application

    return Application()


setup_project()

server = create_server()


if __name__ == "__main__":
    main()
