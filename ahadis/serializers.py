from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from datetime import datetime
from django.shortcuts import get_object_or_404


class QuranSurahSerializer(serializers.Serializer):
    surah_no = serializers.IntegerField()
    surah_name = serializers.CharField(max_length=100)
    no_of_verses = serializers.IntegerField()


class QuranVerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuranVerse
        fields = ['id', 'surah_no', 'surah_name', 'verse_no', 'verse_content']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ['created', 'modified']
        extra_kwargs = {
            'publisher': {'write_only': True},
            'author': {'write_only': True},
            'subject': {'write_only': True},
            'language': {'write_only': True},
            'source_type': {'write_only': True}
        }


class ImamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imam
        fields = ['id', 'name']


class FootNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NarrationFootnote
        fields = ['id', 'expression', 'explanation']


#########################################################################################################
########################################## Narration Subject ############################################

class NarrationSubjectModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NarrationSubject
        fields = ['id', 'subject', 'narration']
        extra_kwargs = {
            'narration': {
                'write_only': True
            }
        }


class NarrationSubjectRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = NarrationSubject
        fields = ['id', 'subject']


class NarrationSubjectListSerializer(serializers.Serializer):
    subjects = serializers.ListField(child=serializers.CharField(max_length=200))


#########################################################################################################

class ContentSummaryTreeSerializer(serializers.ModelSerializer):
    quran_verse = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = ContentSummaryTree
        fields = ['id', 'alphabet', 'subject_1', 'subject_2', 'expression', 'summary', 'narration', 'quran_verse']
        # fields = ['alphabet', 'subject_1', 'subject_2', 'expression', 'summary', 'verse']
        extra_kwargs = {'narration': {'required': False, 'write_only': True}}

    def create(self, validated_data):
        quran_verse_no = validated_data.pop('quran_verse')
        content_summary_tree = ContentSummaryTree.objects.create(**validated_data)
        if quran_verse_no:
            try:
                quran_verse = QuranVerse.objects.get(id=quran_verse_no)
                NarrationSubjectVerse.objects.create(quran_verse=quran_verse, content_summary_tree=content_summary_tree)
            except:
                pass
        return content_summary_tree

    def update(self, instance, validated_data):
        quran_verse_no = validated_data.pop('quran_verse')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if quran_verse_no:
            try:
                quran_verse = QuranVerse.objects.get(id=quran_verse_no)
                narration_subject_verse = NarrationSubjectVerse.objects.get(content_summary_tree=instance)
                narration_subject_verse.quran_verse = quran_verse
                narration_subject_verse.save()
            except:
                pass
        return instance


class NarrationSubjectVerseSerializer(serializers.ModelSerializer):
    quran_verse = QuranVerseSerializer()

    class Meta:
        model = NarrationSubjectVerse
        fields = ['quran_verse']


class ContentSummaryTreeWithVersesSerializer(serializers.ModelSerializer):
    verse = QuranVerseSerializer(source='verse.quran_verse', read_only=True)
    subject = serializers.CharField(max_length=200, source='subject_1')
    sub_subject = serializers.CharField(max_length=200, source='subject_2')

    class Meta:
        model = ContentSummaryTree
        fields = ['id', 'alphabet', 'subject', 'sub_subject', 'expression', 'summary', 'verse']


class NarrationSubjectVersePostSerializer(serializers.Serializer):
    content_summary_tree = ContentSummaryTreeSerializer()
    quran_verse = serializers.IntegerField(required=False)


class ImamRelatedSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'id': value.id,
            'name': value.name,
        }

    def to_internal_value(self, data):
        try:
            return Imam.objects.get(id=data)
        except Imam.DoesNotExist:
            raise serializers.ValidationError('The Imam does not exist')


class BookRelatedSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return {
            'id': value.id,
            'name': value.name,
        }

    def to_internal_value(self, data):
        try:
            return Book.objects.get(id=data)
        except Book.DoesNotExist:
            raise serializers.ValidationError('The book does not exist')


#########################################################################################################
############################################ Narration ##################################################

class NarrationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Narration
        fields = '__all__'


class NarrationRetrieveSerializer(serializers.ModelSerializer):
    footnotes = FootNoteSerializer(many=True, read_only=True)
    subjects = NarrationSubjectModelSerializer(many=True, read_only=True)
    content_summary_tree = ContentSummaryTreeWithVersesSerializer(many=True, read_only=True)

    class Meta:
        model = Narration
        fields = '__all__'
        depth = 2


class NarrationSerializer(serializers.ModelSerializer):
    imam = ImamRelatedSerializer(queryset=Imam.objects.all())
    book = BookRelatedSerializer(queryset=Book.objects.all())
    footnotes = FootNoteSerializer(many=True, required=False)
    subjects = NarrationSubjectRelatedSerializer(many=True, required=False)
    summary_tree = NarrationSubjectVersePostSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Narration
        fields = '__all__'

    def create(self, validated_data):
        footnotes = validated_data.pop('footnotes') if 'footnotes' in validated_data else []
        subjects = validated_data.pop('subjects') if 'subjects' in validated_data else []
        summary_tree = validated_data.pop('summary_tree') if 'summary_tree' in validated_data else []

        narration = Narration.objects.create(**validated_data)
        for footnote in footnotes:
            NarrationFootnote.objects.create(narration=narration, **footnote)

        for subject in subjects:
            NarrationSubject.objects.create(narration=narration, **subject)

        for a in summary_tree:
            content_summary_tree = a.get('content_summary_tree')
            content_summary_tree = ContentSummaryTree.objects.create(**content_summary_tree, narration=narration)
            try:
                quran_verse_id = a.get('quran_verse')
                if quran_verse_id:
                    quran_verse = QuranVerse.objects.get(id=quran_verse_id)
                    NarrationSubjectVerse.objects.create(quran_verse=quran_verse,
                                                         content_summary_tree=content_summary_tree)
                    NarrationVerse.objects.create(narration=narration, quran_verse=quran_verse)
            except:
                pass

        return narration


class FilterOptionsSerializer(serializers.ModelSerializer):
    narration_name = serializers.CharField(source='name')

    imam_name = serializers.CharField(source='imam__name')

    alphabet = serializers.CharField(max_length=200, source='content_summary_tree__alphabet')
    subject = serializers.CharField(max_length=200, source='content_summary_tree__subject_1')
    sub_subject = serializers.CharField(max_length=200, source='content_summary_tree__subject_2')

    surah_name = serializers.CharField(max_length=100, source='content_summary_tree__verse__quran_verse__surah_name')
    verse_no = serializers.IntegerField(source='content_summary_tree__verse__quran_verse__verse_no')
    verse_content = serializers.CharField(source='content_summary_tree__verse__quran_verse__verse_content')

    class Meta:
        model = Narration
        fields = ['narration_name', 'imam_name',
                  'alphabet', 'subject', 'sub_subject',
                  'surah_name', 'verse_no', 'verse_content']


#########################################################################################################


class NarrationFootnoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NarrationFootnote
        fields = '__all__'


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


class VersesSerializer(serializers.Serializer):
    verse_no = serializers.IntegerField()
    verse_content = serializers.CharField()
    sub_subjects = SubSubjectSerializer(many=True)


class AlphabetSerializer(serializers.Serializer):
    alphabet = serializers.CharField(max_length=200)
    subjects = SubjectSerializer(many=True)


class SurahSerializer(serializers.Serializer):
    surah_no = serializers.IntegerField()
    surah_name = serializers.CharField(max_length=200)
    verses = VersesSerializer(many=True)




class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['expires_at'] = datetime.now() + refresh.access_token.lifetime
        data['id'] = self.user.id

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
