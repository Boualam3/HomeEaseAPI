import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import connection, transaction


class Command(BaseCommand):
    help = "Populates database with dummy data"

    def handle(self, *args, **options):
        print("Populating databases...")
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, 'seed.sql')
        try:
            sql = Path(file_path).read_text()
            print('SQL file loaded successfully.')
            sql_commands = sql.replace('\n', '').split(';')
          #   for i in sql_commands:
          #       print(i + "\n")
            with transaction.atomic():  # Start a transaction
                with connection.cursor() as cursor:
                    for command in sql_commands:
                        if not command:
                            continue
                        try:
                            print("cmd : "+command + "\n")
                            cursor.execute(command)
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(
                                f'An error occurred while executing command: {e}'))
                            raise transaction
            print('Database populated successfully.')
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File {file_path} not found'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'An error occurred: {e}'))
