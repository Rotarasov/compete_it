from django.test import TestCase
from events.models import Event
import datetime
from PIL import Image


class EventTestCase(TestCase):
    def setUp(self) -> None:
        Event.objects.create(
            title="Hash Code 2020",
            start_date=datetime.datetime(2020, 5, 22, 19),
            end_date=datetime.datetime(2020, 5, 22, 22),
            description="Hash Code is a team programming competition, organized by Google, \
            for students and professionals around the world. You pick your team \
            and programming language and we pick an engineering problem for you \
            to solve. This year’s contest kicks off with an Online Qualification \
            Round, where your team can compete from wherever you’d like, including \
            from one of our Hash Code hubs. Top teams will then be invited to a Google \
            office for the Final Round",
            type="contest",
            image=Image.open("../media/hash_code"),
            links="https://codingcompetitions.withgoogle.com/hashcode/"
        )
