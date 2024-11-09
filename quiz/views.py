from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Catalog, Test, Question, Choice
from .serializers import CatalogCreateUpdateSerializer, CatalogListSerializer, TestListSerializer, \
    TestCreateUpdateSerializer, QuestionSerializer, \
    ChoiceSerializer
from .permissions import IsUser, IsTeacherOrReadOnly, IsSuperUserOrReadOnly, IsSuperUserOrTeacherOrReadOnly


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()
    permission_classes = [IsAuthenticated, IsSuperUserOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return CatalogListSerializer
        elif self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return CatalogCreateUpdateSerializer
        return CatalogListSerializer


class TestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSuperUserOrTeacherOrReadOnly]

    def get_queryset(self):
        queryset = Test.objects.all()

        catalog_id = self.request.query_params.get('catalog_id', None)
        if catalog_id:
            queryset = queryset.filter(catalog__id=catalog_id)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return TestListSerializer
        elif self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return TestCreateUpdateSerializer
        return TestListSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrReadOnly, IsUser, IsTeacherOrReadOnly]


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrReadOnly, IsUser, IsTeacherOrReadOnly]


class TestResultView(APIView):

    def post(self, request, *args, **kwargs):
        test_id = request.data.get("test_id")
        answers = request.data.get("answers")

        if not test_id or not answers:
            return Response({"detail": "Test ID and answers are required."}, status=status.HTTP_400_BAD_REQUEST)

        test = Test.objects.get(id=test_id)
        correct_answers_count = 0
        total_questions = test.questions.count()

        for question_id, answer_id in answers.items():
            try:
                question = Question.objects.get(id=question_id)
                answer = Answer.objects.get(id=answer_id, question=question)

                if answer.is_correct:
                    correct_answers_count += 1
            except (Question.DoesNotExist, Answer.DoesNotExist):
                continue

        result_percentage = (correct_answers_count / total_questions) * 100 if total_questions > 0 else 0

        return Response({
            "correct_answers": correct_answers_count,
            "total_questions": total_questions,
            "result_percentage": result_percentage,
        })
