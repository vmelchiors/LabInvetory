from django.contrib import admin
from django.urls import path, include
from Core import urls as core_urls
from Inventory import urls as inventory_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(core_urls)),
    path('', include(inventory_urls))
]
