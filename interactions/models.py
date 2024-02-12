from django.contrib.auth.models import User
from django.db import models

from recipes.models import Recipe


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


class Rate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
