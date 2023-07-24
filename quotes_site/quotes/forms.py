from django.forms import ModelForm, CharField, TextInput, ModelMultipleChoiceField, SelectMultiple, Textarea, ValidationError
from .models import Author, Quote, Tag
from django.shortcuts import redirect, reverse


class QuoteForm(ModelForm):
    author = CharField(min_length=5, max_length=150, required=True, widget=TextInput(attrs={'class': 'form-control'}))
    quote = CharField(min_length=5, required=True, widget=Textarea(attrs={'class': 'form-control'}))
    tags = CharField(required=False, widget=TextInput(attrs={'class': 'form-control'}))

    def clean_author(self):
        author_name = self.cleaned_data.get('author')
        if not Author.objects.filter(fullname=author_name).exists():
            raise ValidationError("This author does not exist in the database. Create the author first!")

        return Author.objects.get(fullname=author_name)

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            tags_list = [tag.strip() for tag in tags.split(',')]
            return tags_list
        return ''

    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author']


class AuthorForm(ModelForm):
    fullname = CharField(max_length=40, min_length=5, widget=TextInput(attrs={'class': 'form-control'}))
    born_date = CharField(max_length=25, min_length=12, widget=TextInput(attrs={'class': 'form-control'}))
    born_location = CharField(max_length=150, min_length=12, widget=TextInput(attrs={'class': 'form-control'}))
    description = CharField(widget=Textarea(attrs={'class': 'form-control', 'size': 50}))

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname')
        if Author.objects.filter(fullname=fullname).exists():
            raise ValidationError("This author already exists in the database")
        return fullname

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']

