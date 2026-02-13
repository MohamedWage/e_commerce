from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError

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