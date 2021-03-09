from django.contrib import admin
from .models import postList, comments  # , Like

# Register your models here.
admin.site.register(postList)
admin.site.register(comments)
# admin.site.register(Like)
