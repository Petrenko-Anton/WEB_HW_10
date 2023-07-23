from django.urls import path, include

from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.index, name='main'),  # quotes:main
    path('page/<int:page>', views.index, name='main_paginate'),
    path('author/<str:aut_name>', views.author, name='author'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),
    path('tag/<str:tag_name>/page/<int:page>', views.tag, name='tag_paginate'),
    path('quote/add', views.add_quote, name='add_quote'),
    path('quote/remove/<int:qt_id>', views.del_quote, name='del_quote'),
    path('add_author', views.add_author, name='add_author'),
    path('remove_author/<int:au_id>', views.del_author, name='del_author'),
    ]