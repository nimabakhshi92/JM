from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics


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
