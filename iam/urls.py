from django.urls import path
from .views import LoginView, RefreshTokenView, SignUpView, UserListView, UserView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', RefreshTokenView.as_view(), name='refresh'),
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('user/', UserListView.as_view(), name='user-list'),
    path('user/<int:id>/', UserView.as_view(), name='user-details'),
    path('user/', UserView.as_view(), name='user-create'),

]