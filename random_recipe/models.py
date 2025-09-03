from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    DIFFICULTY = (("easy","쉬움"), ("mid","중간"), ("hard"),("어려움"))
    author = models.
