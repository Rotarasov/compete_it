from django.urls import path
from chats import views

urlpatterns = [
    path('<recipient_id>/', views.MessageList.as_view(), name="chat-room"),
]