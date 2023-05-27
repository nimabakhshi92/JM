from rest_framework import serializers
from .models import *


class FlattenMixin(object):
    """Flatens the specified related objects in this representation"""

    def to_representation(self, obj):
        assert hasattr(self.Meta, 'flatten'), (
            'Class {serializer_class} missing "Meta.flatten" attribute'.format(
                serializer_class=self.__class__.__name__
            )
        )
        # Get the current object representation
        rep = super(FlattenMixin, self).to_representation(obj)
        # Iterate the specified related objects with their serializer
        for field, serializer_class in self.Meta.flatten:
            serializer = serializer_class(context=self.context)
            objrep = serializer.to_representation(getattr(obj, field))
            # Include their fields, prefixed, in the current   representation
            for key in objrep:
                rep[field + "_" + key] = objrep[key]
        return rep


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
        # fields = ['name', 'narrator', 'content', 'book_vol_no', 'book_page_no', 'book_narration_no', 'created',
        #           'modified', 'book', 'imam', 'footnote']
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
