from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ("createdAt", "updatedAt", "deletedAt")


# Register your models here.
admin.site.register(User, UserAdmin)