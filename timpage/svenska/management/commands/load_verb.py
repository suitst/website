from csv import DictReader

from django.core.management import BaseCommand

from svenska.models import Verb

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the question data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables
"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from the substantiv database into the question format."

    def handle(self, *args, **options):
        file_path = input('paste the file path: ')
        file_path = file_path.replace('"', '')
        if Verb.objects.exists():
            max_q = int(max(question.number for question in Verb.objects.all()))
        else:
            max_q = 0
        number = max_q + 1
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = DictReader(file)
            for row in reader:
                question = Verb()
                question.number = number
                number += 1
                question.ord = row['Ord']
                question.engelska = row['På Engelska']
                question.infinitiv = row['Infinitiv']
                question.presens = row['Presens']
                question.imperativ = row['Imperativ']
                question.preteritum = row['Preteritum']
                question.perfekt = row['Perfekt']
                question.pluskvamperfekt = row['Pluskvamperfekt']
                question.save()

        print('Questions loaded')