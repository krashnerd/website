from django.urls import path

from . import views

app_name = 'scrabble'

urlpatterns = [
    path('', views.index, name='index'),
	# path('<int:square_id>/', views.display_id, name = 'display_id'),
	path('<int:square_id>/clicksquare/', views.clicksquare, name = 'clicksquare'),
 ]