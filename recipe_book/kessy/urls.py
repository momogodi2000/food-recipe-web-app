from django.urls import path
from . import views
from .views import ViewRecipeList



urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
    path('propose_recipe/', views.propose_recipe, name='propose_recipe'),
    path('user_panel/', views.user_panel, name='user_panel'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('crud_user/', views.crud_user, name='crud_user'),
    path('crud_recipe/', views.crud_recipe, name='crud_recipe'),
    path('user/create/', views.create_user, name='create_user'),
    path('user/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('user/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('user/<int:user_id>/', views.view_user, name='view_user'),
    path('recipe/create/', views.create_recipe, name='create_recipe'),
    path('recipe/<int:recipe_id>/edit/', views.edit_recipe, name='edit_recipe'),
    path('recipe/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('recipe/<int:recipe_id>/', views.view_recipe, name='view_recipe'),
    path('recipes/', ViewRecipeList.as_view(), name='view_recipe_list'),
]
