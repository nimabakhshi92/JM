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


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer


class TableOfContentsView(APIView):
    # def post(self, request):
    #     print(request.data)
    #     serializer = ContentSummaryTree1FlatSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = ContentSummaryTree.objects.values(
            'alphabet', 'subject_1', 'subject_2', 'expression', 'summary'
        ).distinct().order_by('alphabet', 'subject_1', 'subject_2')

        data = {}
        for item in queryset:
            alphabet = item['alphabet']
            subject = item['subject_1']
            sub_subject = item['subject_2']
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
                    'content': []
                }
                subject_data['sub_subjects'].append(sub_subject_data)

            content_data = {
                'expression': expression,
                'summary': summary
            }
            sub_subject_data['content'].append(content_data)

        serializer = AlphabetSerializer(data=list(data.values()), many=True)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)


class NarrationView(generics.ListAPIView):
    serializer_class = NarrationSerializer

    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        alphabet = self.request.query_params.get('alphabet', None)
        subject = self.request.query_params.get('subject', None)
        sub_subject = self.request.query_params.get('sub_subject', None)
        queryset = Narration.objects.all()
        if alphabet:
            queryset = queryset.filter(content_summary_tree__alphabet=alphabet)
        if subject:
            queryset = queryset.filter(content_summary_tree__subject_1=subject)
        if sub_subject:
            queryset = queryset.filter(content_summary_tree__subject_2=sub_subject)
        return queryset


class MyUserRegisterView(generics.CreateAPIView):
    permission_classes = []

    def create(self, request, *args, **kwargs):
        user_data = request.data
        user_data._mutable = True
        user_data['email'] = user_data.get('username')
        serialized = MyUserRegisterSerializer(data=user_data)

        data = {}

        if serialized.is_valid():
            user = serialized.save()

            data['id'] = user.id
            data['username'] = user.username
            refresh = RefreshToken.for_user(user)
            data['token'] = {
                'token': str(refresh.access_token),
                'refresh_token': str(refresh),
                'expires_at' : datetime.now() + refresh.access_token.lifetime

            }

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serialized.errors
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
