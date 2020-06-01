from django.urls import path
from users import views


urlpatterns = [
    path('login/', views.CustomObtainAuthToken.as_view(), name="login"),
    path('google-login/', views.ObtainGoogleAuthToken.as_view(), name="google-login"),
    path('<int:pk>/', views.UserDetail.as_view(), name="user-detail"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('register/', views.RegisterUser.as_view(), name="register")
]