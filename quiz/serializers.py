from rest_framework import serializers
from .models import Catalog, Test, Question, Choice, TestResults


class ChoiceSerializer(serializers.ModelSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), required=False)

    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct', 'question']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)
    test = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all(), required=False)

    class Meta:
        model = Question
        fields = ['id', 'text', 'test', 'choices']

    def create(self, validated_data):
        print(validated_data)
        choices_data = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)

        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)

        return question


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


class CatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Catalog
        fields = ['id', 'name']


class TestResultsSerializer(serializers.ModelSerializer):
    test_title = serializers.CharField(source='test.title')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = TestResults
        fields = ['id', 'test_title', 'username', 'correct_answers', 'total_questions', 'result_percentage']
