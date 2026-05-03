"""Form blog — apps/blog/forms.py"""
from django import forms
from django.utils.text import slugify
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields = [
            'title', 'slug', 'body', 'excerpt',
            'category', 'tags', 'status', 'cover', 'published_at',
        ]
        widgets = {
            'title':        forms.TextInput(attrs={'class': 'form-control'}),
            'slug':         forms.TextInput(attrs={'class': 'form-control'}),
            'body':         forms.Textarea(attrs={'rows': 20, 'class': 'form-control'}),
            'excerpt':      forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'category':     forms.Select(attrs={'class': 'form-select'}),
            'tags':         forms.SelectMultiple(attrs={'class': 'form-select'}),
            'status':       forms.Select(attrs={'class': 'form-select'}),
            'published_at': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            ),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise forms.ValidationError('Il titolo deve avere almeno 5 caratteri.')
        return title.strip()

    def clean(self):
        cleaned = super().clean()
        # Auto-genera slug se vuoto
        if not cleaned.get('slug') and cleaned.get('title'):
            cleaned['slug'] = slugify(cleaned['title'])
        return cleaned
