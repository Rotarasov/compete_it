from django.urls import path
from chats import views

urlpatterns = [
    path('<int:sender_id>/<receiver_id>', views.MessageList.as_view(), name="chat"),
]