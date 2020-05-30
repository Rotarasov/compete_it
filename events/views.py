from rest_framework import generics, filters, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from events.filters import EventFilter
from events import models
from events import serializers


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






