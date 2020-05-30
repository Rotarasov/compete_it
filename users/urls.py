from django.urls import path, include
from users import views


urlpatterns = [
    path('login/', views.CustomObtainAuthToken.as_view()),
    path('google-login/', include('rest_social_auth.urls_token')),
    path('<int:pk>/', views.UserDetail.as_view()),
    path('logout/', views.Logout.as_view()),
    path('register/', views.RegisterUser.as_view())
]