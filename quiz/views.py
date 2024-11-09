from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Catalog, Test, Question, Choice, TestResults
from .serializers import CatalogSerializer, TestListSerializer, \
    TestCreateUpdateSerializer, QuestionSerializer, \
    ChoiceSerializer, TestResultsSerializer
from .permissions import IsUser, IsSuperUserOrReadOnly, IsSuperUserOrTeacherOrReadOnly


class CatalogViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all().prefetch_related('tests')
    serializer_class = CatalogSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrReadOnly]


class TestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsSuperUserOrTeacherOrReadOnly]

    def get_queryset(self):
        queryset = Test.objects.all().select_related('catalog').prefetch_related('questions')

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
    permission_classes = [IsAuthenticated, IsSuperUserOrTeacherOrReadOnly]

    def get_queryset(self):
        queryset = Question.objects.all().select_related('test').prefetch_related('choices')

        test_id = self.request.query_params.get('test_id', None)
        if test_id:
            queryset = queryset.filter(test_id=test_id)

        return queryset


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all().select_related('question')
    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrTeacherOrReadOnly]


class TestResultView(APIView):
    permission_classes = [IsAuthenticated]

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
                answer = Choice.objects.get(id=answer_id, question=question)

                if answer.is_correct:
                    correct_answers_count += 1
            except (Question.DoesNotExist, Choice.DoesNotExist):
                continue

        result_percentage = (correct_answers_count / total_questions) * 100 if total_questions > 0 else 0
        TestResults.objects.create(user=request.user, test=test, correct_answers=correct_answers_count,
                                   total_questions=total_questions, result_percentage=result_percentage)
        return Response({
            "correct_answers": correct_answers_count,
            "total_questions": total_questions,
            "result_percentage": result_percentage,
        })


class ResultsView(viewsets.ReadOnlyModelViewSet):
    queryset = TestResults.objects.all().prefetch_related('test', 'user')
    serializer_class = TestResultsSerializer
    permission_classes = [IsAuthenticated, IsSuperUserOrTeacherOrReadOnly]
