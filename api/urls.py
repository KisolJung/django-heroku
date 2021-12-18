from django.urls import path, include
from .views import base_views, auth_views as auth, mentor_views as mentor, mentee_views as mentee


user_patterns = [
    # note AUTH
    path('login', auth.LoginView.as_view()),
    path('registration', auth.SignupView.as_view()),
    # note USER
    path('detail/<int:id>', auth.UserDetailView.as_view()),
    path('duplicate/<str:username>', auth.UserDuplicateView.as_view()),
    path('me', auth.UserView.as_view()),
]

board_patterns = [
    path('', mentor.BoardView.as_view()),
    path('/mentee/<int:board_id>', mentee.MenteeView.as_view()),
    path('/detail/<int:board_id>', mentor.BoardDetailView.as_view()),
]


urlpatterns = [
    path('', base_views.IndexView.as_view()),
    path('user/', include(user_patterns)),
    path('board', include(board_patterns)),
]

