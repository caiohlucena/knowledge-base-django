from django.urls import path
from . import views

app_name = 'knowledge'

urlpatterns = [
    path('', views.home, name='home'),
    path('processo/<slug:slug>/', views.process_detail, name='process_detail'),
    path('buscar/', views.search, name='search'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('favorito/<int:pk>/toggle/', views.toggle_favorite, name='toggle_favorite'),
    path('categoria/<slug:slug>/', views.by_category, name='by_category'),
    path('recentes/', views.recent_updates, name='recent_updates'),
    path('processo/novo/', views.create_process, name='create_process'),
    path('processo/<int:pk>/excluir/', views.delete_process, name='delete_process'),
]