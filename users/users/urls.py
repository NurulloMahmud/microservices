from django.urls import path
from .views import CustomTokenObtainPairView, RegisterView, UserInfoView


urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('user/<int:pk>/', UserInfoView.as_view(), name='user_info'),
]
