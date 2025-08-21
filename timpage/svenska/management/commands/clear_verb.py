from django.core.management import BaseCommand
from django.db import transaction

from svenska.models import Verb


class Command(BaseCommand):
    help = "Delete all Verb records (use with caution)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Skip confirmation prompt.",
        )

    def handle(self, *args, **options):
        count = Verb.objects.count()

        if not options["yes"]:
            if count == 0:
                self.stdout.write(self.style.WARNING("No Verb rows to delete."))
                return
            self.stdout.write(f"About to delete Verb: {count}")
            confirm = input('Type "yes" to proceed: ').strip().lower()
            if confirm != "yes":
                self.stdout.write(self.style.WARNING("Aborted."))
                return

        with transaction.atomic():
            deleted_count, _ = Verb.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} Verb rows."))

        self.stdout.write(self.style.SUCCESS("Done."))


