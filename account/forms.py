from django import forms
from django.contrib.auth.models import User


class signupform(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "first_name": forms.TextInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "password": forms.PasswordInput(
                attrs={"class": "form-control form-control-lg"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control form-control-lg"}
            ),

        }
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
