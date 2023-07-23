from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count

from .models import Author, Quote, Tag
from .forms import AuthorForm, QuoteForm


def find_top_ten_tags():
    result_list = []
    top_ten_tags_obj = Tag.objects.annotate(num_quotes=Count('quote')).order_by('-num_quotes')[:10]
    for tag_obj in top_ten_tags_obj:
        result_list.append(tag_obj.name)
    return result_list
# Create your views here.


def index(request, page=1):
    quotes = Quote.objects.all()
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    top_ten_tags = find_top_ten_tags()
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page, "top_ten_tags": top_ten_tags})


def author(request, aut_name):
    author_details = Author.objects.get(fullname=aut_name)
    return render(request, 'quotes/author.html', context={'author': author_details})


def tag(request, tag_name, page=1):
    tag_id=Tag.objects.get(name=tag_name)
    quotes = Quote.objects.filter(tags=tag_id)
    per_page = 5
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    top_ten_tags = find_top_ten_tags()
    return render(request, 'quotes/tag.html', context={'quotes': quotes_on_page, "top_ten_tags": top_ten_tags,
                                                       "tag": tag_name})


@login_required
def add_quote(request):
    form = QuoteForm(instance=Quote())
    if request.method == "POST":
        form = QuoteForm(request.POST, instance=Quote())
        if form.is_valid():
            quote = form.save(commit=False)
            quote.quote = form.cleaned_data.get('quote')
            tags = form.cleaned_data.get('tags')
            quote.author = form.cleaned_data.get('author')
            if not Author.objects.filter(fullname=quote.author.fullname).exists:
                return redirect(to='quotes:add_author', context={'title': 'add new author!',
                                                                 'author': quote.author.fullname})
            quote.save()
            for tag_name in tags:
                tag, created = Tag.objects.get_or_create(name=tag_name)

                if created:
                    tag.save()
                quote.tags.add(tag)

            # Зберегти зміни в зв'язку з тегами
            quote.save()
            return redirect(to='quotes:main')

    return render(request, 'quotes/add_quote.html', context={'title': 'Add Quote', 'form': form})


@login_required
def del_quote(request, qt_id):
    quote = Quote.objects.filter(pk=qt_id)
    quote.delete()
    return redirect(to="quotes:main")


@login_required
def add_author(request):
    form = AuthorForm(instance=Author())
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=Author())
        if form.is_valid():
            author = form.save(commit=False)
            author.fullname = form.cleaned_data.get('fullname')
            author.born_date = form.cleaned_data.get('born_date')
            author.born_location = form.cleaned_data.get('born_location')
            author.save()
            return redirect(to='quotes:main')
    return render(request, 'quotes/add_author.html', context={'title': 'Add Author', 'form': form})



@login_required
def del_author(request, au_id):
    author = Author.objects.filter(pk=au_id)
    author.delete()
    return redirect(to="quotes:main")





