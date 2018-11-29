from django import forms

class TaggerForm(forms.Form):

    paragraph = forms.CharField(label='Paragraph', widget=forms.Textarea)
