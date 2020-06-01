from django.urls import path
from events import views

urlpatterns = [
    path('survey/', views.SurveyQuestionList.as_view(), name="index"),
    path('<int:pk>/', views.EventDetail.as_view(), name="event-detail"),
    path('<int:event_pk>/survey/', views.SurveyAnswer.as_view(), name="survey-answer"),
    path('<int:event_pk>/team-applications/', views.TeamApplicationList.as_view(), name="team-application-list"),
    path('<int:event_pk>/team-applications/<int:user_id>/', views.TeamApplicationDetail.as_view(), name="team-application-detail"),
    path('<int:event_pk>/participation/', views.Participation.as_view(), name="participation")
]