from django.forms import ModelForm, CharField, TextInput, ModelMultipleChoiceField, SelectMultiple, Textarea
from .models import Author, Quote, Tag




class QuoteForm(ModelForm):
    quote = CharField(min_length=5, required=True, widget=TextInput(attrs={'class': 'form-control'}))
    tags = ModelMultipleChoiceField(required=True, queryset=Tag.objects.all(), widget=SelectMultiple)
    author = CharField(min_length=5, max_length=150, required=True, widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author']


class AuthorForm(ModelForm):
    fullname = CharField(max_length=40, min_length=5, widget=TextInput(attrs={'class': 'form-control'}))
    born_date = CharField(max_length=25, min_length=12, widget=TextInput(attrs={'class': 'form-control'}))
    born_location = CharField(max_length=150, min_length=12, widget=TextInput(attrs={'class': 'form-control'}))
    description = CharField(widget=Textarea)

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']