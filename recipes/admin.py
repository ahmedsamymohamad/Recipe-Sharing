from django.contrib import admin
from django.contrib import admin

from .models import Ingredient, Recipe

admin.site.register(Recipe)
admin.site.register(Ingredient)
