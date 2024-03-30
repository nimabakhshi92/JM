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
        fields = ['id', 'alphabet', 'subject_1', 'subject_2', 'subject_3', 'subject_4', 'expression', 'summary',
                  'narration', 'quran_verse']
        extra_kwargs = {'narration': {'required': False, 'write_only': True},
                        'subject_1': {'required': False},
                        'subject_2': {'required': False},
                        'subject_3': {'required': False},
                        'subject_4': {'required': False},
                        'expression': {'required': False},
                        'summary': {'required': False},
                        }

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
        if quran_verse_no == -1:
            try:
                narration_subject_verse = NarrationSubjectVerse.objects.get(content_summary_tree=instance)
                narration_subject_verse.delete()
            except:
                pass
        elif quran_verse_no:
            quran_verse = QuranVerse.objects.get(id=quran_verse_no)
            try:
                narration_subject_verse = NarrationSubjectVerse.objects.get(content_summary_tree=instance)
                narration_subject_verse.quran_verse = quran_verse
                narration_subject_verse.save()
            except:
                narration_subject_verse = NarrationSubjectVerse.objects.create(content_summary_tree=instance,
                                                                               quran_verse=quran_verse)
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
        fields = ['id', 'alphabet', 'subject', 'sub_subject', 'subject_3', 'subject_4', 'expression', 'summary',
                  'verse']


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


class BSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'


class NarrationSerializer(serializers.ModelSerializer):
    imam = ImamRelatedSerializer(queryset=Imam.objects.all())
    book = BookRelatedSerializer(queryset=Book.objects.all())
    footnotes = FootNoteSerializer(many=True, required=False)
    subjects = NarrationSubjectRelatedSerializer(many=True, required=False)
    summary_tree = NarrationSubjectVersePostSerializer(many=True, required=False, write_only=True)
    content_summary_tree = ContentSummaryTreeWithVersesSerializer(many=True, read_only=True)
    is_bookmarked = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.IntegerField(write_only=True)

    bookmarks = BSerializer(many=True, read_only=True)

    class Meta:
        model = Narration
        fields = '__all__'

    def get_is_bookmarked(self, obj):
        if hasattr(obj, 'bookmarks_count'):
            return obj.bookmarks_count > 0

    def create(self, validated_data):
        footnotes = validated_data.pop('footnotes') if 'footnotes' in validated_data else []
        subjects = validated_data.pop('subjects') if 'subjects' in validated_data else []
        summary_tree = validated_data.pop('summary_tree') if 'summary_tree' in validated_data else []
        user_id = validated_data.pop('user_id')

        narration = Narration.objects.create(**validated_data)
        user = User.objects.get(id=user_id)
        narration.owner = user
        narration.save()

        # UserNarration.objects.create(narration=narration,user=user)

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
    # narration_name = serializers.CharField(source='name')

    # imam_name = serializers.CharField(source='imam__name')

    alphabet = serializers.CharField(max_length=200, source='content_summary_tree__alphabet')
    subject = serializers.CharField(max_length=200, source='content_summary_tree__subject_1')

    # sub_subject = serializers.CharField(max_length=200, source='content_summary_tree__subject_2')
    # subject_3 = serializers.CharField(max_length=200, source='content_summary_tree__subject_3')
    # subject_4 = serializers.CharField(max_length=200, source='content_summary_tree__subject_4')
    #
    # surah_name = serializers.CharField(max_length=100, source='content_summary_tree__verse__quran_verse__surah_name')
    # verse_no = serializers.IntegerField(source='content_summary_tree__verse__quran_verse__verse_no')
    # verse_content = serializers.CharField(source='content_summary_tree__verse__quran_verse__verse_content')

    class Meta:
        model = Narration
        # fields = ['narration_name', 'imam_name',
        #           'alphabet', 'subject', 'sub_subject', 'subject_3', 'subject_4',
        #           'surah_name', 'verse_no', 'verse_content']
        fields = ['alphabet', 'subject']


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
    expression = serializers.CharField(allow_blank=True)
    summary = serializers.CharField(allow_blank=True)


class Subject4Serializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, allow_blank=True, trim_whitespace=False)
    content = ContentSerializer(many=True)


class Subject3Serializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, allow_blank=True, trim_whitespace=False)
    subjects_4 = Subject4Serializer(many=True)


class SubSubjectSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, allow_blank=True, trim_whitespace=False)
    subjects_3 = Subject3Serializer(many=True)


class SubSubjectForVerseSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, allow_blank=True)
    content = ContentSerializer(many=True)


class SubjectSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, allow_blank=True, trim_whitespace=False)
    sub_subjects = SubSubjectSerializer(many=True)


class VersesSerializer(serializers.Serializer):
    verse_no = serializers.IntegerField()
    verse_content = serializers.CharField()
    sub_subjects = SubSubjectSerializer(many=True)


class AlphabetSerializer(serializers.Serializer):
    alphabet = serializers.CharField(max_length=200, default='', trim_whitespace=False)
    subjects = SubjectSerializer(many=True, default='')


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
        data['is_staff'] = self.user.is_staff

        return data


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.token_class(attrs["refresh"])
        data['expires_at'] = datetime.now() + refresh.access_token.lifetime

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


class BookmarkSerializer(serializers.ModelSerializer):
    narration = NarrationSerializer(read_only=True)
    narration_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Bookmark
        # fields = ['id', 'narration', 'narration_id']
        fields = ['id', 'narration', 'narration_id', 'user_id']
        extra_kwargs = {'user': {'write_only': True}}
        # depth = 2

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        narration_id = validated_data.pop('narration_id')
        narration = Narration.objects.get(pk=narration_id)
        user = User.objects.get(id=user_id)

        created = Bookmark.objects.create(user=user, narration=narration)
        return created

# class UserNarrationSerializer(serializers.ModelSerializer):
#     narration = NarrationSerializer(read_only=True)
#     narration_id = serializers.IntegerField(write_only=True)
#     user_id = serializers.IntegerField(write_only=True)
#
#     class Meta:
#         model = UserNarration
#         # fields = ['id', 'narration', 'narration_id']
#         fields = ['id', 'narration', 'narration_id', 'user_id']
#         extra_kwargs = {'user': {'write_only': True}}
#         # depth = 2
#
#     def create(self, validated_data):
#         user_id = validated_data.pop('user_id')
#         narration_id = validated_data.pop('narration_id')
#         narration = Narration.objects.get(pk=narration_id)
#         user = User.objects.get(id=user_id)
#
#         created = UserNarration.objects.create(user=user, narration=narration)
#         return created
