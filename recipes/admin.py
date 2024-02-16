from django.contrib import admin
from django.contrib import admin
from .models import CacheEntry

from .models import Ingredient, Recipe

admin.site.register(Recipe)
admin.site.register(Ingredient)


@admin.register(CacheEntry)
class CacheEntryAdmin(admin.ModelAdmin):
    list_display = ('key', 'expiration')