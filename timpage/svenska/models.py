from django.db import models

class user(models.Model):
    username = models.CharField()
    email = models.CharField()

    def __str__(self):
        return self.username
