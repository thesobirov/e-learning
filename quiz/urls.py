from django.urls import path
from .views import CatalogViewSet, TestViewSet, QuestionViewSet, ChoiceViewSet, TestResultView, ResultsView

urlpatterns = [
    path('catalogs/', CatalogViewSet.as_view({'get': 'list', 'post': 'create'}), name='catalog-list'),
    path('catalogs/<int:pk>/', CatalogViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='catalog-detail'),

    path('tests/', TestViewSet.as_view({'get': 'list', 'post': 'create'}), name='test-list'),
    path('tests/<int:pk>/', TestViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='test-detail'),

    path('questions/', QuestionViewSet.as_view({'get': 'list', 'post': 'create'}), name='question-list'),
    path('questions/<int:pk>/', QuestionViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='question-detail'),

    path('choices/', ChoiceViewSet.as_view({'get': 'list', 'post': 'create'}), name='choice-list'),
    path('choices/<int:pk>/', ChoiceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='choice-detail'),

    path('test-execution/', TestResultView.as_view(), name='test-execution'),

    path('results/', ResultsView.as_view({'get': 'list'}), name='results'),

]
