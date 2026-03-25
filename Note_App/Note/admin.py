from django.contrib import admin
from Note.models  import Note
from Note.form import NoteForm
# Register your models here.
class FormAdmin(admin.ModelAdmin):
    # Note=NoteForm  # OLD - wrong syntax, should use list_display
    list_display = ['title', 'content']
admin.site.register(Note,FormAdmin)