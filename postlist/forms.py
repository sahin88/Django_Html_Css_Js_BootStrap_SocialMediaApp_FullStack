from .models import postList
from django import forms


class postForm(forms.ModelForm):
    class Meta:
        model = postList
        fields = ['image', 'video', 'video_link', 'caption', 'created_date']


class ContactForm(forms.Form):

    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea)
