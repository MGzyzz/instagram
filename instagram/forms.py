from django import forms
from instagram.models import Comment, Publication

class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        label='Найти',
        widget=forms.TextInput(attrs={
            'class': 'form-control my-3',
            'placeholder': 'enter search value'
        })
    )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'publication', 'text']


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['image', 'description']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control mb-3'}),
            'description': forms.TextInput(attrs={'class': 'form-control mb-3'}),
        }