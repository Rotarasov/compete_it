from django.urls import path
from events.views import EventList, EventDetail

urlpatterns = [
    path('', EventList.as_view()),
    path('<int:pk>', EventDetail.as_view())
]