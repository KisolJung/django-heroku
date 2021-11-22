from django.urls import path, include
from .views import base_views, auth_views as auth, mentor_views as mentor


user_patterns = [
    # note AUTH
    path('login', auth.LoginView.as_view()),
    path('registration', auth.SignupView.as_view()),
    # note USER
    path('detail/<int:id>', auth.UserDetailView.as_view()),
    path('duplicate/<str:username>', auth.UserDuplicateView.as_view()),
    path('me', auth.UserView.as_view()),
]

board_pattenrs = [
    path('mentor/', mentor.MentorView.as_view()),
]

urlpatterns = [
    path('', base_views.IndexView.as_view()),
    path('user/', include(user_patterns)),
    path('board/', include(board_pattenrs)),
]

