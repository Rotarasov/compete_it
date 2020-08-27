from django.contrib import admin

from .models import Event, SurveyQuestion, TeamApplication, SurveyAnswer, Participation

admin.site.register(Event)
admin.site.register(Participation)
admin.site.register(SurveyQuestion)
admin.site.register(SurveyAnswer)
admin.site.register(TeamApplication)
