from django.contrib import admin
from .models import Notes


# Register your models here.
class NotesAdmin(admin.ModelAdmin):
    list_display = ['id', 'notes', 'created_at', 'updated_at']


admin.site.register(Notes, NotesAdmin)
