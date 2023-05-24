from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(label="Email")
    subject = forms.CharField(max_length=100, label="Objet", help_text="100 caractères max")
    message = forms.CharField(label="Message", max_length=5000, help_text="5000 caractères max", widget=forms.Textarea)
