from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Initialize BDD"

    def handle(self, *args, **options):
        print("Reset database")
        call_command("reset_db", "--noinput", "-c")
        print("Reset successful")

        print("Apply migrations")
        call_command("migrate", interactive=False)
