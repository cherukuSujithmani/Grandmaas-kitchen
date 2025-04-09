
from django import forms
from .models import Account,Address
from django.contrib.auth.hashers import make_password

# Registration Form
class Regform(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'address', 'password']

    def save(self, commit=True):
        account = super().save(commit=False)
        account.set_password(self.cleaned_data['password'])  # Use set_password()
        if commit:
            account.save()
        return account

# Login Form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)  # Adjusted max_length
    password = forms.CharField(widget=forms.PasswordInput()) # Adjusted max_length

# address form fields
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['full_name', 'street', 'city', 'state', 'postal_code', 'country', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'street': forms.TextInput(attrs={'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Postal Code'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        }
