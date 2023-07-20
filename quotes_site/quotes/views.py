from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Author, Quote, Tag
from .forms import AuthorForm, QuoteForm


# Create your views here.
def index(request):
    quotes = Quote.objects.all()
    tags = Quote.tags.all()
    return render(request, 'quotes/index.html', context={'quotes': quotes, 'tags': tags})


def author(request):
    ...


def tag(request):
    ...


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


