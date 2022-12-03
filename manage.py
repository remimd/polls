import sys

from sources.infrastructure.setup import setup_project


def main():
    setup_project()

    from django.core.management import execute_from_command_line

    execute_from_command_line(argv=sys.argv)


if __name__ == "__main__":
    main()
