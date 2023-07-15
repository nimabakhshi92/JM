from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['name', 'publisher']


class ImamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imam
        fields = ['name']


class FootNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = NarrationFootnote
        fields = ['expression', 'explanation']


class NarrationSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NarrationSubject


class NarrationSerializer(serializers.ModelSerializer):
    imam = ImamSerializer()
    book = BookSerializer()
    footnote = FootNoteSerializer(many=True)

    class Meta:
        model = Narration
        fields = '__all__'


# ////////////////////////////////// API
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
