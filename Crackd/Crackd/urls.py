from django.contrib import admin
from django.urls import path, include
from game import views as game_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', game_views.mineView, name='home'),
    path('inventory/', game_views.inventoryView, name='inventory'),
    path('synth-lab/', game_views.synthLabView, name='synth-lab'),
    path('buildings/', game_views.buildingsView, name='buildings'),
    path('research/', game_views.researchView, name='research'),
    path('company/', game_views.companyView, name='company'),
    path('collections/', game_views.collectionsView, name='collections'),
    path('shop/', game_views.shopView, name='shop'),
    path('market/', game_views.marketView, name='market'),
    path('catalog/', game_views.catalogView, name='catalog'),
    path('leaderboard/', game_views.leaderboardView, name='leaderboard'),
]
