from django.db import models
from django.contrib.auth.models import AbstractUser
from svenska.models import Substantiv, Verb


class CustomUser(AbstractUser):
    total_answered = models.IntegerField(default=0)

    total_substantiv_answered = models.IntegerField(default=0)
    total_verb_answered = models.IntegerField(default=0)

    engelska_correct = models.IntegerField(default=0)
    engelska_incorrect = models.IntegerField(default=0)

    obestamt_singular_correct = models.IntegerField(default=0)
    obestamt_singular_incorrect = models.IntegerField(default=0)

    bestamt_singular_correct = models.IntegerField(default=0)
    bestamt_singular_incorrect = models.IntegerField(default=0)

    obestamt_plural_correct = models.IntegerField(default=0)
    obestamt_plural_incorrect = models.IntegerField(default=0)

    bestamt_plural_correct = models.IntegerField(default=0)
    bestamt_plural_incorrect = models.IntegerField(default=0)

    infinitv_correct = models.IntegerField(default=0)
    infinitiv_incorrect = models.IntegerField(default=0)

    presens_correct = models.IntegerField(default=0)
    presens_incorrect = models.IntegerField(default=0)

    imperativ_correct = models.IntegerField(default=0)
    imperativ_incorrect = models.IntegerField(default=0)

    preteritum_correct = models.IntegerField(default=0)
    preteritum_incorrect = models.IntegerField(default=0)

    perfekt_correct = models.IntegerField(default=0)
    perfekt_incorrect = models.IntegerField(default=0)

    pluskvamperfekt_correct = models.IntegerField(default=0)
    pluskvamperfekt_incorrect = models.IntegerField(default=0)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def update_total(self, word):
        self.total_answered += 1
        if type(word) == Substantiv:
            self.total_substantiv_answered += 1
        elif type(word) == Verb:
            self.total_verb_answered += 1
        self.save()

    
    def update_record(self, result, field):
        field_mapping = {
            'engelska_result': ('engelska_correct', 'engelska_incorrect'),
            'infinitiv_result': ('infinitiv_correct', 'infinitiv_incorrect'),
            'presens_result': ('presens_correct', 'presens_incorrect'),
            'imperativ_result': ('imperativ_correct', 'imperativ_incorrect'),
            'preteritum_result': ('preteritum_correct', 'preteritum_incorrect'),
            'perfekt_result': ('perfekt_correct', 'perfekt_incorrect'),
            'pluskvamperfekt_result': ('pluskvamperfekt_correct', 'pluskvamperfekt_incorrect')
        }
        print(f'field: {field}')
        if field in field_mapping:
            correct_field, incorrect_field = field_mapping[field]
            if result:
                setattr(self, correct_field, getattr(self, correct_field) + 1)
                print(f'cheese {field:}: {getattr(self, correct_field)}')
            else:
                setattr(self, incorrect_field, getattr(self, incorrect_field) + 1)
                print(f'cheese {field:}: {getattr(self, incorrect_field)}')
        self.save()
        print(f'Updated {field} with {result} result')




        

