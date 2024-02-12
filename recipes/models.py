from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


class Recipe(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField()
    description = models.TextField(max_length=4000)
    ingredients = models.ManyToManyField("Ingredient")

    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    EASY = "0"
    MEDIUM = "1"
    HARD = "2"
    DIFFICULTY_CHOICES = [
        (EASY, "Easy"),
        (MEDIUM, "Medium"),
        (HARD, "Hard"),
    ]
    difficulty = models.CharField(
        max_length=1, choices=DIFFICULTY_CHOICES, default=EASY,
    )

    def __str__(self):
        return self.name

    def get_avg_rate(self):
        avg = self.rate_set.aggregate(Avg("rate"))["rate__avg"]
        return round(avg, 2) if avg is not None else 0


class Ingredient(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name
