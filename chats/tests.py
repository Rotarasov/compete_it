from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from users.models import User
from .models import ChatRoom, Message

class APIChatTestCase(APITestCase):
    def setUp(self) -> None:
        self.u1 = User.objects.create_user('u1@gmail.com', 'John', 'Watson', 'p1')
        self.u2 = User.objects.create_user('u2@gmail.com', 'Vasil', 'Zelenskiy', 'p2')
        self.chat_room = ChatRoom.objects.create()
        self.chat_room.members.add(self.u1, self.u2)
        Message.objects.create(chat_room=self.chat_room, sender=self.u1, message='Hello!')
        Message.objects.create(chat_room=self.chat_room, sender=self.u2, message='Hey! What`s up?')

    def test_base(self):
        chat_room = (ChatRoom.objects.filter(members=self.u1) &
                     ChatRoom.objects.filter(members=self.u2)).first()
        self.assertIsNotNone(chat_room)

        message_u1 = Message.objects.filter(chat_room=chat_room, sender=self.u1).first()
        self.assertEqual(message_u1.message, 'Hello!')

        message_u2 = Message.objects.filter(chat_room=chat_room, sender=self.u2).first()
        self.assertEqual(message_u2.message, 'Hey! What`s up?')

    def test_getting_all_messages(self):
        token = Token.objects.create(user=self.u1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('chat-room', args=[self.u2.id])
        response = self.client.get(url)
        self.assertEqual(response.data['count'], 2)





