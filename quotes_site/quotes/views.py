from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
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
    name = aut_name.replace('%20',' ')
    author_details = Author.objects.get(fullname=name)
    return render(request, 'quotes/author.html', context={'author': author_details})


def tag(request, tag_name, page=1):
    tag_id=Tag.objects.get(name=tag_name)
    quotes = Quote.objects.filter(tags=tag_id)
    per_page = 10
    paginator = Paginator(list(quotes), per_page)
    quotes_on_page = paginator.page(page)
    top_ten_tags = find_top_ten_tags()
    return render(request, 'quotes/tag.html', context={'quotes': quotes_on_page, "top_ten_tags": top_ten_tags,
                                                       "tag": tag_name})


@login_required
def add_quote(request):
    ...


@login_required
def del_quote(request):
    ...


@login_required
def add_author(request):
    ...


@login_required
def del_author(request):
    ...

@login_required
def add_tag(request):
    ...

@login_required
def del_tag(request):
    ...


