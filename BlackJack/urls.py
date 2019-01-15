"""BlackJack URL Configuration"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from GameManager.views import GameManagerLoginView, GameManagerLogoutView, GameManagerRegistrationView, GameCreateView, GameListView, \
    GameListPageView, FastGameCreateView
from BlackJack import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', GameManagerLoginView.as_view(), name='login'),
    path('logout/', GameManagerLogoutView.as_view(), name='logout'),
    path('registration/', GameManagerRegistrationView.as_view(), name='registration'),
    path('games_list/<str:whose>/', GameListView.as_view(), name='game_list'),
    path('games_list/<str:whose>/page/',
         GameListPageView.as_view(), name='game_page'),
    path('game_creation/', GameCreateView.as_view(), name='game_creation'),
    path('fast_game_creation/',
         FastGameCreateView.as_view(success_url='/fast_game_creation/'),
         name='fast_game_creation'),
    path('profile/', include(('GameManager.profile_urls', 'P'))),
    path('<int:id>/', include(('GameManager.game_urls', 'GameManager'))),
    path('', GameManagerLoginView.as_view(), name='login'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
