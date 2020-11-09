from django.contrib import admin
from mytest.models import users

# Register your models here.

class usersAdmin(admin.ModelAdmin):
    list_display=('uid', 'question')
admin.site.register(users, usersAdmin)
