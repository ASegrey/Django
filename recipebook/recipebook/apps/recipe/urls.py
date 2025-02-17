from django.urls import path
from . import views

app_name = 'recipes'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:recipe_id>/', views.detail, name = 'detail'),
    path('<int:recipe_id>/leave_comment/', views.leave_comment, name = 'leave_comment'),
    path('add/', views.add_recipe, name='add_recipe'),
    path('<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
]
