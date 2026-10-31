from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "name",
            "email",
            "phone",
            "message",
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Your full name"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "example@example.com"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+234 000 0000 000"
            }),

            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Tell me about your project"
            })
        }
