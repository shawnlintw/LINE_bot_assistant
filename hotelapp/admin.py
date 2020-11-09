from django.contrib import admin
# Register your models here.
class clientAdmin(admin.ModelAdmin):
    list_display=('uid', 'dataset')
admin.site.register(client, clientAdmin)

