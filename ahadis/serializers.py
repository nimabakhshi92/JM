from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from datetime import datetime
from django.shortcuts import get_object_or_404


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ImamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imam
        fields = ['id', 'name']


class FootNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NarrationFootnote
        fields = ['expression', 'explanation']


# NOT needed yet.
# class NarrationSubjectSerializer1(serializers.ModelSerializer):
#     class Meta:
#         model = NarrationSubject
#         fields = ['subject']
#         # fields = '__all__'


class NarrationSubjectSerializer(serializers.Serializer):
    subjects = serializers.ListField(child=serializers.CharField(max_length=200))


class NarrationSubjectSerializer2(serializers.Serializer):
    subjects = serializers.CharField(max_length=200)


class ContentSummaryTreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentSummaryTree
        fields = ['alphabet', 'subject_1', 'subject_2', 'expression', 'summary']


class NarrationSerializer(serializers.ModelSerializer):
    imam = ImamSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    imam_id = serializers.IntegerField(write_only=True)
    book_id = serializers.IntegerField(write_only=True)

    footnote = FootNoteSerializer(many=True, read_only=True)

    class Meta:
        model = Narration
        fields = '__all__'

    def create(self, validated_data):
        imam_id = validated_data.pop('imam_id')
        book_id = validated_data.pop('book_id')

        # footnote_data = validated_data.pop('footnote', [])
        # content_summary_tree_data = validated_data.pop('content_summary_tree', [])
        # subjects_data = validated_data.pop('subjects', [])

        try:
            imam = Imam.objects.get(pk=imam_id)
        except Imam.DoesNotExist:
            raise serializers.ValidationError('The imam_id does not exist')

        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            raise serializers.ValidationError('The book_id does not exist')

        narration = Narration.objects.create(imam=imam, book=book, **validated_data)

        # for footnote in footnote_data:
        #     expression = footnote.get('expression')
        #     explanation = footnote.get('explanation')
        #     NarrationFootnote.objects.create(narration=narration, expression=expression, explanation=explanation)
        #
        # for subject in subjects_data:
        #     NarrationSubject.objects.create(narration=narration, subject=subject)
        #
        # for tree in content_summary_tree_data:
        #     alphabet = tree.get('alphabet')
        #     subject_1 = tree.get('subject_1')
        #     subject_2 = tree.get('subject_2')
        #     expression = tree.get('expression')
        #     summary = tree.get('summary')
        #     ContentSummaryTree.objects.create(narration=narration, alphabet=alphabet, subject_1=subject_1,
        #                                       subject_2=subject_2, expression=expression, summary=summary)

        return narration


# class NarrationDetailSerializer(serializers.ModelSerializer):
#     imam = ImamSerializer()
#     book = BookSerializer()
#     footnote = FootNoteSerializer(many=True)
#
#     class Meta:
#         model = Narration
#         fields = '__all__'

class ContentSerializer(serializers.Serializer):
    expression = serializers.CharField()
    summary = serializers.CharField()


class SubSubjectSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = ContentSerializer(many=True)


class SubjectSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    sub_subjects = SubSubjectSerializer(many=True)


class AlphabetSerializer(serializers.Serializer):
    alphabet = serializers.CharField(max_length=200)
    subjects = SubjectSerializer(many=True)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['expires_at'] = datetime.now() + refresh.access_token.lifetime

        return data


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.token_class(attrs["refresh"])
        data['expires_aat'] = datetime.now() + refresh.access_token.lifetime

        return data


class MyUserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        return user


class QuranSurahSerializer(serializers.Serializer):
    surah_no = serializers.IntegerField()
    surah_name = serializers.CharField(max_length=100)
    no_of_verses = serializers.IntegerField()


class QuranVerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuranVerse
        fields = ['id', 'surah_no', 'surah_name', 'verse_no', 'verse_content']

#
# class BookSerializer1(serializers.ModelSerializer):
#
#     class Meta:
#         model = Book1
#         fields = '__all__'
#
#
# class ImamSerializer2(serializers.ModelSerializer):
#     class Meta:
#         model = Imam1
#         fields = '__all__'
#
#
# class NarrationSubject1Serializer1(serializers.ModelSerializer):
#     class Meta:
#         model = NarrationSubject1
#         fields = '__all__'
#
#
# class NarrationSerializer1(serializers.ModelSerializer):
#     imam = ImamSerializer2()
#     book = BookSerializer1()
#     subjects = NarrationSubject1Serializer1(many=True, read_only=True)
#
#     class Meta:
#         model = Narration1
#         fields = ['id', 'name', 'book', 'imam', 'subjects']
#
#
# class ImamSerializer1(serializers.ModelSerializer):
#     narration = NarrationSerializer1(many=True, read_only=True)
#
#     class Meta:
#         model = Imam1
#         fields = ['name', 'narration']
#         # exclude = ('narration', )
#
#
# class ContentSummaryTree1Serializer(serializers.ModelSerializer):
#     # narration = NarrationSerializer1(many=True, read_only=True)
#     subjects = serializers.SerializerMethodField()
#
#     class Meta:
#         model = ContentSummaryTree1
#         fields = ['alphabet', 'subjects']
#         # exclude = ('narration', )
#
#     def get_subjects(self, obj):
#         # queryset = ContentSummaryTree1.objects.filter(alphabet=obj.get('alphabet'))
#         # return [item.subject_1 for item in queryset]
#         queryset = ContentSummaryTree1.objects.filter(alphabet=obj.get('alphabet')).values_list('subject_1', flat=True)
#         return list(queryset)
#
#
# class ContentSummaryTree1FlatSerializer(serializers.ModelSerializer):
#     # narration = NarrationSerializer1(many=True, read_only=True)
#
#     class Meta:
#         model = ContentSummaryTree1
#         fields = '__all__'
#         # exclude = ('narration', )
