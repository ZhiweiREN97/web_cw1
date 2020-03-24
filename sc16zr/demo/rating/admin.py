from django.contrib import admin

# Register your models here.

from .models import Professor, Module, User, Score
admin.site.register(Professor)
admin.site.register(Module)
admin.site.register(User)
admin.site.register(Score)
