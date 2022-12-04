import logging

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Initialize BDD"
    logger = logging.getLogger("init_bdd")

    def handle(self, *args, **options):
        self.logger.warning("Reset database")
        call_command("reset_db", "--noinput", "-c")
        self.logger.info("Reset successful")

        self.logger.info("Apply migrations")
        call_command("migrate", interactive=False)
