from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    
    
    class Meta:
        model = User
        fields = ('email','first_name','second_name')
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("the email already exist")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if any(char.isdigit() for char in first_name):
            raise ValidationError("first name must be char only")
        if len(first_name) < 3:
            raise ValidationError("the first name must be more than 2")
        return first_name

    def clean_second_name(self):
        second_name = self.cleaned_data.get('second_name')
        if any(char.isdigit() for char in second_name):
            raise ValidationError("second name must be char only")
        if len(second_name) < 3:
            raise ValidationError("the second name must be more than 2")
        return second_name
    
    
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data