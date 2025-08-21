from django.core.management import BaseCommand
from django.db import transaction

from svenska.models import Substantiv


class Command(BaseCommand):
    help = "Delete all Substantiv records (use with caution)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Skip confirmation prompt.",
        )

    def handle(self, *args, **options):
        count = Substantiv.objects.count()

        if not options["yes"]:
            if count == 0:
                self.stdout.write(self.style.WARNING("No Substantiv rows to delete."))
                return
            self.stdout.write(f"About to delete Substantiv: {count}")
            confirm = input('Type "yes" to proceed: ').strip().lower()
            if confirm != "yes":
                self.stdout.write(self.style.WARNING("Aborted."))
                return

        with transaction.atomic():
            deleted_count, _ = Substantiv.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} Substantiv rows."))

        self.stdout.write(self.style.SUCCESS("Done."))


