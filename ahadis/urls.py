from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from django.views.decorators.cache import cache_page
from . import views
from . import viewsets
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
app_name = 'ahadis'

# router = DefaultRouter()
# router.register('book1', viewsets.Books1VS, basename='book-1')
# router.register('imam1', viewsets.Imam1VS, basename='imam-1')
# router.register('narration1', viewsets.Narration1VS, basename='narration1')
# router.register('subjects1', viewsets.NarrationSubject1VS, basename='subjects1')
# router.register('table_of_contents', viewsets.ContentSummaryTree1VS, basename='table_of_contents')

urlpatterns = [
    # path('api/', include(router.urls)),
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

    #     //////////////////////////////////////////// API
    # path('Book1', viewsets.Books1VS.as_view(), name='book-1')
    path('api/token/', viewsets.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', viewsets.MyTokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', viewsets.MyUserRegisterView.as_view(), name='register'),

    path('api/table_of_contents/', viewsets.TableOfContentsView.as_view(), name='table_of_contents'),
    path('api/narrations_list/', viewsets.NarrationView.as_view(), name='narrations_list'),
    # path('api/login/', obtain_auth_token)

]
