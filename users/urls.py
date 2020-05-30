from django.urls import path
from users import views


urlpatterns = [
    path('login/', views.CustomObtainAuthToken.as_view()),
    path('google-login/', views.ObtainGoogleAuthToken.as_view()),
    path('<int:pk>/', views.UserDetail.as_view()),
    path('logout/', views.Logout.as_view()),
    path('register/', views.RegisterUser.as_view())
]