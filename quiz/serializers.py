from rest_framework import serializers
from .models import Catalog, Test, Question, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']


class TestCreateUpdateSerializer(serializers.ModelSerializer):
    catalog = serializers.PrimaryKeyRelatedField(queryset=Catalog.objects.all(), required=False)

    class Meta:
        model = Test
        fields = ['id', 'title', 'catalog']

    def update(self, instance, validated_data):
        title = validated_data.get('title', instance.title)
        catalog = validated_data.get('catalog', instance.catalog)

        instance.title = title
        instance.catalog = catalog

        instance.save()
        return instance


class TestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'title']


class CatalogCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ['id', 'name']


class CatalogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ['id', 'name']
