from django.contrib import admin

# Register your models here.

from store.models import Book

admin.site.register(Book)