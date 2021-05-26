from django import forms


class CreateNewsForm(forms.Form):
    text = forms.CharField(label="text", max_length=1024)
    title = forms.CharField(label="title", max_length=1024)


class SearchNewsForm(forms.Form):
    q = forms.CharField(label="q", max_length=1024)
