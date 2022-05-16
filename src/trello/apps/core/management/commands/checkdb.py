import time

from django.core.management import BaseCommand
from django.db.utils import OperationalError as DjangoOperationalError
from psycopg2 import OperationalError as PostgresOperationalError


class Command(BaseCommand):
    """Django command to pause execution until database is available"""
    def handle(self, *args, **options):
        self.stdout.write(self.style.ERROR("Checking database connection..."))
        up = False
        while up is False:
            try:
                self.check(databases=['default'])
                up = True
            except(DjangoOperationalError, PostgresOperationalError):
                self.stdout.write(self.style.FAILURE("Database is not ready yet, waiting..."))
            time.sleep(2)
        self.stdout.write(self.style.SUCCESS("Database is ready now!"))
