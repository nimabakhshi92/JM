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
        fields = '__all__'


class ImamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imam
        fields = '__all__'


# class NarrationSerializer(serializers.ModelSerializer):
#     book = BookSerializer()
#     imam = ImamSerializer()
#     narration = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Narration
#         fields = ('book', 'narration', 'imam')
#
#     def get_narration(self, obj):
#         return obj


# class NarrationSerializer(serializers.HyperlinkedModelSerializer):
#     imam_name = serializers.Field(source='imam.name')
#     imam_created = serializers.Field(source='imam.created')
#
#     class Meta:
#         model = Narration
#         fields = ('id', 'narrator', 'content', 'imam_name', 'imam_created')


# class NarrationSerializer(serializers.ModelSerializer):
#     imam = ImamSerializer()
#
#     class Meta:
#         model = Narration
#         fields = ('id', 'narrator', 'content', 'imam')
#
#     def to_representation(self, instance):
#         data = super(NarrationSerializer, self).to_representation(instance)
#         imam = data.pop('imam')
#         for key, val in imam.items():
#             data.update({key: val})
#         return data


# class NarrationSubjectSerializer(serializers.ModelSerializer):
#     narration = NarrationSerializer()
#     narration_subject = serializers.SerializerMethodField()
#
#     class Meta:
#         model = NarrationSubject
#         fields = ('narration', 'narration_subject')
#
#     def get_narration_subject(self, obj):
#         return obj

class NarrationSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = NarrationSubject


# class NarrationSerializer(FlattenMixin, serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Narration
#         fields = ('id', 'name', 'narrator', 'content', 'book_vol_no', 'book_page_no', 'book_narration_no')
#         flatten = [('imam', ImamSerializer), ('narrationsubject', NarrationSubjectSerializer)]

#
# class NarrationSerializer(serializers.HyperlinkedModelSerializer):
#     imam_name = serializers.Field(source='imam.name')
#     imam_created = serializers.Field(source='imam.created')
#
#     class Meta:
#         model = Narration
#         fields = ('id', 'narrator', 'content', 'imam_name', 'imam_created')

# class NarrationSerializer(serializers.ModelSerializer):
#     imam = ImamSerializer()
#     narrationsubject = NarrationSubjectSerializer()
#
#     class Meta:
#         model = Narration
#         fields = ('id', 'narrator', 'content', 'imam', 'narrationsubject')
#
#     def to_representation(self, instance):
#         data = super(NarrationSerializer, self).to_representation(instance)
#         imam = data.pop('imam')
#         for key, val in imam.items():
#             data.update({key: val})
#         narrationsubject = data.pop('narrationsubject')
#         for key, val in narrationsubject.items():
#             data.update({key: val})
#         return data

class NarrationSerializer(serializers.ModelSerializer):
    imam = ImamSerializer()


    class Meta:
        model = Narration
        fields = '__all__'
