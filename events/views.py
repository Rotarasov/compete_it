from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters, permissions, status, mixins
from rest_framework.response import Response

from events import models
from events import serializers
from events.filters import EventFilter
from users.models import User


class EventList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EventFilter
    search_fields = ['title', 'description', 'type']

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs['fields'] = ['id', 'title', 'start_date', 'type', 'image']
        return serializer_class(*args, **kwargs)


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = serializers.EventSerializer
    queryset = models.Event.objects.all()

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        kwargs['fields'] = '__all__'
        return serializer_class(*args, **kwargs)


class SurveyQuestionList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = models.SurveyQuestion.objects.all()
    serializer_class = serializers.SurveyQuestionSerializer


class SurveyAnswer(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.SurveyAnswerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        participation = models.Participation.objects.get(id=serializer.data['participation'])
        passed_questions = models.SurveyAnswer.objects.filter(participation_id=participation).count()
        if passed_questions == 3:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        passed_survey = False
        all_questions = models.SurveyQuestion.objects.all().count()
        if passed_questions == all_questions:
            passed_survey = True
        participation.passed_survey = passed_survey
        return Response({'passed_survey': passed_survey, **serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)


class TeamApplicationList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.TeamApplicationSerializer

    def get_queryset(self):
        return models.TeamApplication.objects.filter(participation__event_id=self.kwargs.get('event_pk'))

    def create(self, request, *args, **kwargs):
        event = generics.get_object_or_404(models.Event, pk=request.data.get('event_pk'))
        user = generics.get_object_or_404(User, pk=request.data.get('user_id'))
        participation = generics.get_object_or_404(models.Participation, user=user, event=event)
        team_application = models.TeamApplication.objects.filter(participation=participation).first()
        if team_application is not None:
            return Response({'details': 'Team application for this user already exists'},
                            status=status.HTTP_409_CONFLICT)
        data = {'participation': participation.id, 'description': request.data.get('description')}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class TeamApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.TeamApplicationSerializer
    queryset = models.TeamApplication.objects.all()

    def get_object(self):
        participation = generics.get_object_or_404(models.Participation,
                                                   user_id=self.kwargs.get('user_id'),
                                                   event_id=self.kwargs.get('event_pk'))
        return generics.get_object_or_404(models.TeamApplication, participation=participation)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.participation.user != self.request.user:
            return Response({'details': 'This user is not allowed to update this team application'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.participation.user != self.request.user:
            return Response({'details': 'This user is not allowed to delete this team application'},
                            status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class Participation(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ParticipationSerializer
    queryset = models.Participation.objects.all()

    def get_object(self):
        user_id = self.request.user.id
        return models.Participation.objects.filter(user_id=user_id,
                                            event_id=self.kwargs.get('event_pk')).first()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'details': 'User does not participate in this event'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user_id = self.request.user.id
        participation = models.Participation.objects.filter(user_id=user_id,
                                                            event_id=self.kwargs.get('event_pk')).first()
        if participation is not None:
            return Response({'details': "User already participates in this event"},
                            status=status.HTTP_400_BAD_REQUEST)
        data = {'user': user_id, 'event': self.kwargs.get('event_pk')}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def delete(self, request, *args, **kwargs):
        participation = self.get_object()
        if participation is None:
            return Response({'details': "User does not participate in this event yet"},
                            status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(participation)
        return Response(status=status.HTTP_204_NO_CONTENT)