from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'ahadis'
urlpatterns = [
    path('save_hadis_page', cache_page(60000)(views.save_hadis_page), name='save_hadis_page'),
    path('show', views.show, name='show'),
    path('save_book_page', cache_page(60000)(views.save_book_page), name='save_book_page'),
    path('save_hadis', views.save_hadis, name='save_hadis'),
    path('save_book', views.save_book, name='save_book'),
    path('search', views.search, name='search'),
    path('filter_ahadis_from_fehrest', views.filter_ahadis_from_fehrest, name='filter_ahadis_from_fehrest'),
    path('filter_ahadis_from_fehrest_subject', views.filter_ahadis_from_fehrest_subject, name='filter_ahadis_from_fehrest_subject'),
    path('check_hadis_repetition', views.check_hadis_repetition, name='check_hadis_repetition'),
    # path('test', views.test, name='test'),
]
