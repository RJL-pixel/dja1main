

from django.urls import path

from users.views import UsersListCreateView, UserRetrieveUpdataDestroyView

urlpatterns = [
       path('users', UsersListCreateView.as_view()),
       path('users/<int:pk>', UserRetrieveUpdataDestroyView.as_view())
]
