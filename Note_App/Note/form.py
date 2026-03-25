from django import forms
from Note.models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model=Note
        fields=['title','content'] 