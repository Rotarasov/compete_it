from django.test import TestCase
from events.models import Event
import datetime
import pytz


class EventTestCase(TestCase):
    def setUp(self) -> None:
        Event.objects.create(
            title="Hash Code 2020",
            start_date=datetime.datetime(2020, 5, 22, 19, tzinfo=pytz.UTC),
            end_date=datetime.datetime(2020, 5, 22, 22, tzinfo=pytz.UTC),
            description="Hash Code is a team programming competition, organized by Google, \
            for students and professionals around the world. You pick your team \
            and programming language and we pick an engineering problem for you \
            to solve. This year’s contest kicks off with an Online Qualification \
            Round, where your team can compete from wherever you’d like, including \
            from one of our Hash Code hubs. Top teams will then be invited to a Google \
            office for the Final Round",
            type="contest",
            image="event_pics/hash_code.jpg",
            link="https://codingcompetitions.withgoogle.com/hashcode/"
        )
        Event.objects.create(
            title="Code Jam 2020",
            start_date=datetime.datetime(2020, 6, 10, 19, tzinfo=pytz.UTC),
            end_date=datetime.datetime(2020, 6, 10, 22, tzinfo=pytz.UTC),
            description="Code Jam is Google's longest running global coding competition, \
            where programmers of all levels put their skills to the test. Competitors work \
            their way through a series of online algorithmic puzzles to earn a spot at the World \
            Finals, all for a chance to win the championship title and $15,000.",
            type="contest",
            image="event_pics/code_jam.jpg",
            link="https://codingcompetitions.withgoogle.com/hashcode/"
        )
