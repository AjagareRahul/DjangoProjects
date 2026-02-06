from django import forms
from django.contrib.auth.models import User
from accounts.models import Material
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
class Materials(forms.ModelForm):
    class Meta:
        model=Material
        fields=['name','price','description','image']
        
