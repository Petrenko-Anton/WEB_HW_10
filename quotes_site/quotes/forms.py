from django.forms import ModelForm, CharField, TextInput, ModelMultipleChoiceField, SelectMultiple, Textarea, ValidationError
from .models import Author, Quote, Tag
from django.shortcuts import redirect, reverse


class QuoteForm(ModelForm):
    author = CharField(min_length=5, max_length=150, required=True, widget=TextInput(attrs={'class': 'form-control'}))
    quote = CharField(min_length=5, required=True, widget=Textarea(attrs={'class': 'form-control'}))
    tags = ModelMultipleChoiceField(required=True, queryset=Tag.objects.all(),
                                    widget=SelectMultiple(attrs={'class': 'form-control'}))

    def clean_author(self):
        author_name = self.cleaned_data.get('author')
        # Перевіряємо, чи автор з таким іменем вже існує в базі даних
        if not Author.objects.filter(fullname=author_name).exists():
            # Якщо автор не існує, перенаправляємо користувача на сторінку вводу нового автора
            return redirect(reverse('create_author'))

        return author_name

    class Meta:
        model = Quote
        fields = ['quote', 'tags', 'author']


class AuthorForm(ModelForm):
    fullname = CharField(max_length=40, min_length=5, widget=TextInput(attrs={'class': 'form-control'}))
    born_date = CharField(max_length=25, min_length=12, widget=TextInput(attrs={'class': 'form-control'}))
    born_location = CharField(max_length=150, min_length=12, widget=TextInput(attrs={'class': 'form-control'}))
    description = CharField(widget=Textarea(attrs={'class': 'form-control'}))

    def clean_fullname(self):
        fullname = self.cleaned_data.get('fullname')
        if Author.objects.filter(fullname=fullname).exists():
            raise ValidationError("Such author already exists in the database")
        return fullname

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']

class TagForm(ModelForm):
    name = CharField(max_length=40, min_length=2, widget=TextInput(attrs={'class': 'form-control'}))

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Tag.objects.filter(name=name).exists():
            raise ValidationError("Such Tag already exists in the database")
        return name

    class Meta:
        model = Tag
        fields = ['name']
