from django.db import models

class user(models.Model):
    username = models.CharField()
    email = models.CharField()

    def __str__(self):
        return self.username

class Substantiv(models.Model):
    number = models.IntegerField()
    category = models.CharField()
    ord = models.CharField()
    engelska = models.CharField()
    obestämt_singular = models.CharField()
    bestämt_singular = models.CharField()
    obestämt_plural = models.CharField()
    bestämt_plural = models.CharField()

    def __str__(self):
        return self.ord
