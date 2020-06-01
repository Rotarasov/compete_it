from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls import url
from django.conf import settings
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from events import views

schema_view = get_schema_view(
   openapi.Info(
      title="Compete IT API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="roman.tarasov1@nure.ua"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', views.EventList.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('events/', include('events.urls')),
    path('chats/', include('chats.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)