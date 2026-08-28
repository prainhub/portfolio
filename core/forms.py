from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Your name", "autocomplete": "name"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "you@example.com", "autocomplete": "email"}
            ),
            "subject": forms.TextInput(attrs={"placeholder": "What's this about?"}),
            "message": forms.Textarea(
                attrs={"placeholder": "Tell me a bit about the opportunity or project…", "rows": 6}
            ),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return name

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("Message is too short — add a little more detail.")
        if len(message) > 4000:
            raise forms.ValidationError("Message is too long (max 4000 characters).")
        return message
