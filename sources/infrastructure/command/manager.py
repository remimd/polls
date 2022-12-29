class CommandManager:
    def execute(self, *argv):
        from django.core.management import execute_from_command_line

        execute_from_command_line(argv=argv)
