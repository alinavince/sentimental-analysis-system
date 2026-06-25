from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.PredictSentimentView.as_view(), name='predict'),
    path('history/', views.AnalysisHistoryView.as_view(), name='history'),
    path('stats/', views.StatisticsView.as_view(), name='stats'),
    path('history/<int:pk>/', views.DeleteAnalysisView.as_view(), name='delete-analysis'),
    path('health/', views.HealthCheckView.as_view(), name='health'),
]