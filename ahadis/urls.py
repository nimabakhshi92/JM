from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from . import viewsets

app_name = 'ahadis'

router = DefaultRouter()
router.register('book', viewsets.BookVS, basename='book')
router.register('imam', viewsets.ImamVS, basename='imam')
router.register('subject', viewsets.SubjectVS, basename='subjects')
router.register('quran_surah', viewsets.QuranSurahVS, basename='quran_surah')
router.register('quran', viewsets.QuranVS, basename='quran')
router.register('narration', viewsets.NarrationVS, basename='narration')
router.register('footnote', viewsets.NarrationFootnoteVS)
router.register('summary_tree', viewsets.ContentSummaryTreeVS)
router.register('bookmark', viewsets.BookmarkVS, basename='bookmark')
router.register('shared_narrations', viewsets.SharedNarrationsVS, basename='shared_narrations')
# router.register('heavy_speed_test2', viewsets.HeavySpeedTestVS, basename='heavy_speed_test2')

# router.register('narration1', viewsets.Narration1VS, basename='narration1')
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
    path('api/register/', viewsets.MyUserRegisterView.as_view(), name='register'),
    path('api/login/', viewsets.MyTokenObtainPairView.as_view(), name='login'),
    path('api/token/refresh/', viewsets.MyTokenRefreshView.as_view(), name='token_refresh'),

    path('api/table_of_contents/', viewsets.TableOfContentsView.as_view(), name='table_of_contents'),
    path('api/verses_table_of_contents/', viewsets.VersesTableOfContentsView.as_view(),
         name='verses_table_of_contents'),
    path('api/surah_table_of_contents/', viewsets.SurahTableOfContentsView.as_view(),
         name='surah_table_of_contents'),

    # path('api/narrations_list/', viewsets.NarrationVS.as_view(), name='narrations_list'),
    path('api/', include(router.urls)),
    path('api/filter_options/', viewsets.FilterOptionsVS.as_view(), name='test'),
    path('api/similar_narrations/', viewsets.SimilarNarrations.as_view(), name='similar_narrations'),
    path('api/duplicate_narration/<int:narration_id>/', viewsets.DuplicateNarrationVS.as_view(),
         name='duplicate_narration'),
    path('api/move_narration_to_main_site/<int:narration_id>/', viewsets.MoveToMainSiteNarrationVS.as_view(),
         name='move_narration_to_main_site'),
    path('api/download_narrations/', viewsets.DownloadNarrationVS.as_view(), name='download_narrations'),
    path('api/speed_test/', viewsets.SpeedTestVS.as_view(), name='speed_test'),
    path('api/heavy_speed_test2/', viewsets.HeavySpeedTestVS.as_view(), name='heavy_speed_test2'),
]
