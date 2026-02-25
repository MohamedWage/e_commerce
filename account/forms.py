from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
class UserValidation:
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            if any(char.isdigit() for char in first_name):
                raise ValidationError("First name must be letters only.")
            if len(first_name) < 3:
                raise ValidationError("First name must be more than 2 characters.")
        return first_name

    def clean_second_name(self):
        second_name = self.cleaned_data.get('second_name')
        if second_name:
            if any(char.isdigit() for char in second_name):
                raise ValidationError("Second name must be letters only.")
            if len(second_name) < 3:
                raise ValidationError("Second name must be more than 2 characters.")
        return second_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if hasattr(self, 'instance') and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            raise ValidationError("This email already exists.")
        return email

class SignUpForm(UserValidation, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'second_name')

class UserUpdateForm(UserValidation, forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'second_name', 'email')
        
        
class VerifyForm(forms.Form):
    code = forms.CharField(
        max_length=6, 
        min_length=6, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter 6-digit code', 'class': 'form-control'})
    )



class ForgetPassForm(forms.Form):
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'enter your email'
        })
    )
    
    
    
class NewPassForm(forms.Form):
    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        confirm = cleaned_data.get("confirm_password")

        if password and confirm and password != confirm:
            self.add_error('confirm_password', "Passwords do not match!")

        if password:
            try:
                validate_password(password)
            except exceptions.ValidationError as e:
                self.add_error('new_password', e)

        return cleaned_data