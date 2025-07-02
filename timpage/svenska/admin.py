from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser
from .models import Substantiv, Verb

admin.site.register(CustomUser, UserAdmin)

@admin.register(Substantiv)
class SubstantivAdmin(admin.ModelAdmin):
    list_display = ('ord', 'category', 'engelska', )

@admin.register(Verb)
class VerbAdmin(admin.ModelAdmin):
    list_display = ('ord', 'engelska')