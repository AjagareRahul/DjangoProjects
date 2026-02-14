from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UserProfile, Address, ProductReview


class UserProfileForm(forms.ModelForm):
    """Form for user profile"""
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    
    class Meta:
        model = UserProfile
        fields = ['phone', 'alternate_phone', 'profile_image', 'date_of_birth', 'gender']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self.instance, 'user'):
            self.initial['first_name'] = self.instance.user.first_name
            self.initial['last_name'] = self.instance.user.last_name
            self.initial['email'] = self.instance.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email', '')
        user.save()
        if commit:
            profile.save()
        return profile


class AddressForm(forms.ModelForm):
    """Form for user addresses"""
    class Meta:
        model = Address
        fields = ['name', 'phone', 'address_type', 'address', 'landmark', 'city', 'state', 'pincode', 'is_default']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class ProductReviewForm(forms.ModelForm):
    """Form for product reviews"""
    class Meta:
        model = ProductReview
        fields = ['rating', 'title', 'review']
        widgets = {
            'review': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'rating-input'})
        self.fields['title'].widget.attrs.update({'placeholder': 'Review Title'})
        self.fields['review'].widget.attrs.update({'placeholder': 'Write your review...'})


class UserRegistrationForm(UserCreationForm):
    """Custom user registration form"""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=False)
    phone = forms.CharField(max_length=15, required=False)
    
    class Meta:
        model = UserCreationForm.Meta.model
        fields = ('username', 'email', 'first_name', 'last_name', 'phone', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            UserProfile.objects.create(user=user, phone=self.cleaned_data.get('phone', ''))
        return user
