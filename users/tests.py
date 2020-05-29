from django.test import TestCase
from .models import User


class UserTestCase(TestCase):
    def setUp(self) -> None:
        User.objects.create(
            email='user@gmail.com',
            first_name='John',
            last_name='Snow',
            password='testuser1'
        )
        User.objects.create_superuser(
            email='admin@gmail.com',
            first_name='Walter',
            last_name='Disney',
            password='testadmin1'
        )
