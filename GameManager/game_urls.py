from django.urls import path

from GameManager.views import GameView, GameRemoveView, GameJoinView, GameLeaveView

urlpatterns = [
    path('leave/', GameLeaveView.as_view(), name='game_leave'),
    path('remove/', GameRemoveView.as_view(), name='game_remove'),
    path('join/', GameJoinView.as_view(), name='game_join'),
    path('', GameView.as_view(), name='game_url'),
]
