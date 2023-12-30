import json

from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import mixins, viewsets
from django.db.models import Max
from .pagination import *
from .views import *
from rest_framework import filters

class BaseCreateUpdateDestroyVS(viewsets.GenericViewSet, mixins.CreateModelMixin,
                                mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    pass


class BaseListCreateUpdateDestroyVS(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                                    mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    pass


class BaseListCreateRetrieveUpdateDestroyVS(viewsets.GenericViewSet,
                                            mixins.RetrieveModelMixin,
                                            mixins.ListModelMixin,
                                            mixins.CreateModelMixin,
                                            mixins.DestroyModelMixin,
                                            mixins.UpdateModelMixin):
    pass


class MyUserRegisterView(generics.CreateAPIView):
    permission_classes = []

    def create(self, request, *args, **kwargs):
        user_data = request.data
        user_data._mutable = True
        user_data['username'] = user_data.get('email')
        serialized = MyUserRegisterSerializer(data=user_data)

        data = {}

        if serialized.is_valid():
            user = serialized.save()

            data['id'] = user.id
            data['username'] = user.username
            data['email'] = user.email
            refresh = RefreshToken.for_user(user)
            data['token'] = {
                'token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'expires_at': datetime.now() + refresh.access_token.lifetime

            }

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serialized.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer


class TableOfContentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = ContentSummaryTree.objects.values(
            'alphabet', 'subject_1', 'subject_2', 'subject_3', 'subject_4', 'expression', 'summary'
        ).distinct().order_by('alphabet', 'subject_1', 'subject_2', 'subject_3', 'subject_4')

        data = {}
        for item in queryset:
            alphabet = item['alphabet']
            subject = item['subject_1']
            sub_subject = item['subject_2']
            subject_3 = item['subject_3']
            subject_4 = item['subject_4']
            expression = item['expression']
            summary = item['summary']

            if alphabet not in data:
                data[alphabet] = {
                    'alphabet': alphabet,
                    'subjects': []
                }

            alphabet_data = data[alphabet]
            subject_data = next(
                (sub for sub in alphabet_data['subjects'] if sub['title'] == subject),
                None
            )

            if subject_data is None:
                subject_data = {
                    'title': subject,
                    'sub_subjects': []
                }
                alphabet_data['subjects'].append(subject_data)

            sub_subject_data = next(
                (sub for sub in subject_data['sub_subjects'] if sub['title'] == sub_subject),
                None
            )

            if sub_subject_data is None:
                sub_subject_data = {
                    'title': sub_subject,
                    'subjects_3': []
                }
                subject_data['sub_subjects'].append(sub_subject_data)

            subjects_3_data = next(
                (sub for sub in sub_subject_data['subjects_3'] if sub['title'] == subject_3),
                None
            )

            if subjects_3_data is None:
                subjects_3_data = {
                    'title': subject_3,
                    'subjects_4': []
                }
                sub_subject_data['subjects_3'].append(subjects_3_data)

            subjects_4_data = next(
                (sub for sub in subjects_3_data['subjects_4'] if sub['title'] == subject_4),
                None
            )

            if subjects_4_data is None:
                subjects_4_data = {
                    'title': subject_4,
                    'content': []
                }
                subjects_3_data['subjects_4'].append(subjects_4_data)

            content_data = {
                'expression': expression,
                'summary': summary
            }
            subjects_4_data['content'].append(content_data)

        serializer = AlphabetSerializer(data=list(data.values()), many=True)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)


class SurahTableOfContentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = NarrationSubjectVerse.objects.filter(content_summary_tree__alphabet='بیان').values(
            'quran_verse__surah_no', 'quran_verse__surah_name', 'quran_verse__verse_no', 'quran_verse__verse_content',
            'content_summary_tree__subject_3', 'content_summary_tree__subject_4',
            'content_summary_tree__subject_2', 'content_summary_tree__expression', 'content_summary_tree__summary',
        ).distinct().order_by('quran_verse__surah_no', 'quran_verse__verse_no',
                              'content_summary_tree__subject_2', 'content_summary_tree__subject_3',
                              'content_summary_tree__subject_4')

        data = {}
        for item in queryset:
            surah_no = item['quran_verse__surah_no']
            surah_name = item['quran_verse__surah_name']
            verse_no = item['quran_verse__verse_no']
            verse_content = item['quran_verse__verse_content']
            sub_subject = item['content_summary_tree__subject_2']
            subject_3 = item['content_summary_tree__subject_3']
            subject_4 = item['content_summary_tree__subject_4']
            expression = item['content_summary_tree__expression']
            summary = item['content_summary_tree__summary']

            if surah_no not in data:
                data[surah_no] = {
                    'surah_no': surah_no,
                    'surah_name': surah_name,
                    'verses': []
                }

            surah_data = data[surah_no]
            verses_data = next(
                (sub for sub in surah_data['verses'] if sub['verse_no'] == verse_no),
                None
            )

            if verses_data is None:
                verses_data = {
                    'verse_no': verse_no,
                    'verse_content': verse_content,
                    'sub_subjects': []
                }
                surah_data['verses'].append(verses_data)

            sub_subject_data = next(
                (sub for sub in verses_data['sub_subjects'] if sub['title'] == sub_subject),
                None
            )

            if sub_subject_data is None:
                sub_subject_data = {
                    'title': sub_subject,
                    'subjects_3': []
                }
                verses_data['sub_subjects'].append(sub_subject_data)

            subjects_3_data = next(
                (sub for sub in sub_subject_data['subjects_3'] if sub['title'] == subject_3),
                None
            )

            if subjects_3_data is None:
                subjects_3_data = {
                    'title': subject_3,
                    'subjects_4': []
                }
                sub_subject_data['subjects_3'].append(subjects_3_data)

            subjects_4_data = next(
                (sub for sub in subjects_3_data['subjects_4'] if sub['title'] == subject_4),
                None
            )

            if subjects_4_data is None:
                subjects_4_data = {
                    'title': subject_4,
                    'content': []
                }
                subjects_3_data['subjects_4'].append(subjects_4_data)

            content_data = {
                'expression': expression,
                'summary': summary
            }
            subjects_4_data['content'].append(content_data)

        serializer = SurahSerializer(data=list(data.values()), many=True)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)


class VersesTableOfContentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = NarrationSubjectVerse.objects.values(
            'content_summary_tree__alphabet', 'content_summary_tree__subject_1', 'content_summary_tree__subject_2',
            'content_summary_tree__subject_3', 'content_summary_tree__subject_4',
            'content_summary_tree__expression', 'content_summary_tree__summary'
        ).distinct().order_by('content_summary_tree__alphabet', 'content_summary_tree__subject_1',
                              'content_summary_tree__subject_2', 'content_summary_tree__subject_3',
                              'content_summary_tree__subject_4')

        data = {}
        for item in queryset:
            alphabet = item['content_summary_tree__alphabet']
            subject = item['content_summary_tree__subject_1']
            sub_subject = item['content_summary_tree__subject_2']
            subject_3 = item['content_summary_tree__subject_3']
            subject_4 = item['content_summary_tree__subject_4']
            expression = item['content_summary_tree__expression']
            summary = item['content_summary_tree__summary']

            if alphabet not in data:
                data[alphabet] = {
                    'alphabet': alphabet,
                    'subjects': []
                }

            alphabet_data = data[alphabet]
            subject_data = next(
                (sub for sub in alphabet_data['subjects'] if sub['title'] == subject),
                None
            )

            if subject_data is None:
                subject_data = {
                    'title': subject,
                    'sub_subjects': []
                }
                alphabet_data['subjects'].append(subject_data)

            sub_subject_data = next(
                (sub for sub in subject_data['sub_subjects'] if sub['title'] == sub_subject),
                None
            )

            if sub_subject_data is None:
                sub_subject_data = {
                    'title': sub_subject,
                    'subjects_3': []
                }
                subject_data['sub_subjects'].append(sub_subject_data)

            subjects_3_data = next(
                (sub for sub in sub_subject_data['subjects_3'] if sub['title'] == subject_3),
                None
            )

            if subjects_3_data is None:
                subjects_3_data = {
                    'title': subject_3,
                    'subjects_4': []
                }
                sub_subject_data['subjects_3'].append(subjects_3_data)

            subjects_4_data = next(
                (sub for sub in subjects_3_data['subjects_4'] if sub['title'] == subject_4),
                None
            )

            if subjects_4_data is None:
                subjects_4_data = {
                    'title': subject_4,
                    'content': []
                }
                subjects_3_data['subjects_4'].append(subjects_4_data)

            content_data = {
                'expression': expression,
                'summary': summary
            }
            subjects_4_data['content'].append(content_data)

        serializer = AlphabetSerializer(data=list(data.values()), many=True)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)


class NarrationVS(BaseListCreateRetrieveUpdateDestroyVS):
    permission_classes = [IsAuthenticated]
    pagination_class = MyPagination

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return NarrationRetrieveSerializer
        elif self.action == 'update':
            return NarrationUpdateSerializer
        else:
            return NarrationSerializer

    def get_queryset(self):
        alphabet = self.request.query_params.get('alphabet', None)
        subject = self.request.query_params.get('subject', None)
        sub_subject = self.request.query_params.get('sub_subject', None)
        subject_3 = self.request.query_params.get('subject_3', None)
        subject_4 = self.request.query_params.get('subject_4', None)
        imam_name = self.request.query_params.get('imam_name', None)
        narration_name = self.request.query_params.get('narration_name', None)
        surah_name = self.request.query_params.get('surah_name', None)
        verse_no = self.request.query_params.get('verse_no', None)
        subjects_search = self.request.query_params.get('subjects_search', None)
        texts_search = self.request.query_params.get('texts_search', None)
        queryset = Narration.objects.all()
        if alphabet:
            queryset = queryset.filter(content_summary_tree__alphabet=alphabet)
        if subject:
            queryset = queryset.filter(content_summary_tree__subject_1=subject)
        if sub_subject:
            queryset = queryset.filter(content_summary_tree__subject_2=sub_subject)
        if subject_3:
            queryset = queryset.filter(content_summary_tree__subject_3=subject_3)
        if subject_4:
            queryset = queryset.filter(content_summary_tree__subject_4=subject_4)
        if imam_name:
            queryset = queryset.filter(imam__name=imam_name)
        if narration_name:
            queryset = queryset.filter(name=narration_name)
        if surah_name:
            queryset = queryset.filter(narrationverse__quran_verse__surah_name=surah_name)
        if verse_no:
            queryset = queryset.filter(narrationverse__quran_verse__verse_no=verse_no)
        if subjects_search:
            for or_subject_list in subjects_search.split(','):
                queryset = queryset.filter(subjects__subject__in=or_subject_list.split('|'))
        if texts_search:
            original_queryset = queryset
            for or_text_list_str in texts_search.split(','):
                filtered_queryset = []
                or_text_list = or_text_list_str.split('|')
                for item in queryset:
                    for text in or_text_list:
                        if remove_arabic_characters(text) in remove_arabic_characters(item.content):
                            filtered_queryset.append(item)
                            break
                queryset = filtered_queryset
            queryset = original_queryset.filter(id__in=map(lambda x: x.id, queryset))
        return queryset.distinct().order_by('-modified')


class BookVS(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
             viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class ImamVS(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ImamSerializer
    queryset = Imam.objects.all()


class SubjectVS(BaseListCreateUpdateDestroyVS):
    permission_classes = [IsAuthenticated]
    serializer_class = NarrationSubjectModelSerializer
    queryset = NarrationSubject.objects.all()

    def list(self, request, *args, **kwargs):
        subjects = NarrationSubject.objects.values_list('subject', flat=True).distinct()
        serializer = NarrationSubjectListSerializer({'subjects': subjects})
        return Response(serializer.data)


class QuranSurahVS(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = QuranSurahSerializer
    queryset = QuranVerse.objects.values('surah_no', 'surah_name').annotate(no_of_verses=Max('verse_no'))


class QuranVS(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = QuranVerseSerializer

    def get_queryset(self):
        surah_no = self.request.query_params.get('surah_no')
        verse_no = self.request.query_params.get('verse_no')

        queryset = QuranVerse.objects.all()
        if surah_no:
            queryset = queryset.filter(surah_no=surah_no)
        if verse_no:
            queryset = queryset.filter(verse_no=verse_no)

        return queryset


class NarrationFootnoteVS(BaseCreateUpdateDestroyVS):
    queryset = NarrationFootnote.objects.all()
    serializer_class = NarrationFootnoteSerializer
    permission_classes = [IsAuthenticated]


class ContentSummaryTreeVS(BaseListCreateUpdateDestroyVS):
    serializer_class = ContentSummaryTreeSerializer
    queryset = ContentSummaryTree.objects.all()
    permission_classes = [IsAuthenticated]


class FilterOptionsVS(generics.ListAPIView):
    serializer_class = FilterOptionsSerializer
    permission_classes = [IsAuthenticated]
    queryset = Narration.objects.all().values('name',
                                              'imam__name',
                                              'content_summary_tree__alphabet',
                                              'content_summary_tree__subject_1',
                                              'content_summary_tree__subject_2',
                                              'content_summary_tree__subject_3',
                                              'content_summary_tree__subject_4',
                                              'content_summary_tree__verse__quran_verse__surah_name',
                                              'content_summary_tree__verse__quran_verse__verse_no',
                                              'content_summary_tree__verse__quran_verse__verse_content').distinct()
