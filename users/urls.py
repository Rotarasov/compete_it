from django.urls import path, include
from users import views


urlpatterns = [
    path('api-token-auth/', views.CustomObtainAuthToken.as_view()),
    path('', include('rest_social_auth.urls_token')),
]