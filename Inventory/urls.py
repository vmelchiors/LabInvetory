from django.urls import path, include
from Inventory import views as inventory_views

category_patterns = [
    path('categories/', inventory_views.category_list, name='category_list'),
    path('categories/new/', inventory_views.category_create, name='category_create'),
    path('categories/<int:pk>/edit/', inventory_views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', inventory_views.category_delete, name='category_delete'),
]

material_patterns = [
    path('materials/', inventory_views.material_list, name='material_list'),
    path('materials/new/', inventory_views.material_create, name='material_create'),
    path('materials/<int:pk>/', inventory_views.material_detail, name='material_detail'),
    path('materials/<int:pk>/edit/', inventory_views.material_update, name='material_update'),
    path('materials/<int:pk>/delete/', inventory_views.material_delete, name='material_delete'),
]

loan_patterns = [
    path('loans/', inventory_views.loan_list, name='loan_list'),
    path('loans/new/', inventory_views.loan_create, name='loan_create'),
    path('loans/<int:pk>/', inventory_views.loan_detail, name='loan_detail'),
    path('loans/<int:pk>/return/', inventory_views.loan_return, name='loan_return'),
    path('my-loans/', inventory_views.my_loans, name='my_loans'),
]

urlpatterns = [
    path('', inventory_views.dashboard, name='dashboard'),
]+ category_patterns + material_patterns + loan_patterns