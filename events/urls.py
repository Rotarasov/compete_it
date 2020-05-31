from django.urls import path
from events import views

urlpatterns = [
    path('', views.EventList.as_view()),
    path('survey/', views.SurveyQuestionList.as_view()),
    path('<int:pk>/', views.EventDetail.as_view()),
    path('<int:event_pk>/survey/', views.SurveyAnswer.as_view()),
    path('<int:event_pk>/team-applications/', views.TeamApplicationList.as_view()),
    path('<int:event_pk>/team-applications/<int:user_id>/', views.TeamApplicationDetail.as_view()),
    path('<int:event_pk>/participation/', views.Participation.as_view())
]