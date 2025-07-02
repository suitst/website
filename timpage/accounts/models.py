from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    total_answered = models.IntegerField(default=0)

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

    def update_total(self):
        self.total_answered += 1
        self.save()
    
    def update_record(self, result, field):
        field_mapping = {
        'engelska_result': ('engelska_correct', 'engelska_incorrect'),
        'obestamt_singular_result': ('obestamt_singular_correct', 'obestamt_singular_incorrect'),
        'bestamt_singular_result': ('bestamt_singular_correct', 'bestamt_singular_incorrect'),
        'obestamt_plural_result': ('obestamt_plural_correct', 'obestamt_plural_incorrect'),
        'bestamt_plural_result': ('bestamt_plural_correct', 'bestamt_plural_incorrect')
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




        

