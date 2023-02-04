from django.urls import path
from django.views.decorators.cache import cache_page
from . import views

app_name = 'ahadis'
urlpatterns = [
    path('save_hadis_page', views.save_narration_page, name='save_hadis_page'),
    path('save_hadis', views.save_narration, name='save_hadis'),
    path('', views.show, name='show'),
    path('save_book_page', views.save_book_page, name='save_book_page'),
    path('save_book', views.save_book, name='save_book'),
    # path('save_imams', views.save_imam, name='save_imam'),
    path('search', views.search, name='search'),
    path('filter_ahadis_from_fehrest', views.filter_ahadis_from_fehrest, name='filter_ahadis_from_fehrest'),
    path('filter_ahadis_from_fehrest_subject', views.filter_ahadis_from_fehrest_subject,
         name='filter_ahadis_from_fehrest_subject'),
    path('filter_ayat_from_fehrest_subject', views.filter_ayat_from_fehrest_subject,
         name='filter_ayat_from_fehrest_subject'),
    path('filter_ahadis_from_fehrest_subject_a', views.filter_ahadis_from_fehrest_subject_a,
         name='filter_ahadis_from_fehrest_subject_a'),
    path('filter_ahadis_from_fehrest_subject_b', views.filter_ahadis_from_fehrest_subject_b,
         name='filter_ahadis_from_fehrest_subject_b'),
    path('check_hadis_repetition', views.check_hadis_repetition, name='check_hadis_repetition'),
    # path('test', views.test, name='test'),
]
