from django.db import models


class UserData(models.Model):
    login = models.CharField(max_length=50, unique=True)
    password = models.IntegerField()
