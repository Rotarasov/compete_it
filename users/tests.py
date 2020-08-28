from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import User


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='user@gmail.com',
            first_name='John',
            last_name='Snow',
            password='testuser1'
        )
        self.admin = User.objects.create_superuser(
            email='admin@gmail.com',
            first_name='Walter',
            last_name='Disney',
            password='testadmin1'
        )

    def test_default_image(self):
        assert 'default' in self.user.image

    def test_getting_user_profile(self):
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        print(response.data)
        img = response.data['image']
        assert 'default' in img



