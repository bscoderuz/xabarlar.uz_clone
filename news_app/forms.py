from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']

#
# class ContactFrom(forms.Form):
#     name = forms.CharField(max_length=200)
#     email = forms.EmailField()
#     subject = forms.Textarea()
