from django.urls import path, include
from Inventory import views as inventory_views

category_patterns = [
    path('categories/', inventory_views.category_list, name='category_list'),
    path('categories/new/', inventory_views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', inventory_views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', inventory_views.category_delete, name='category_delete'),
]

urlpatterns = [
    path('', inventory_views.dashboard, name='dashboard'),
]+ category_patterns