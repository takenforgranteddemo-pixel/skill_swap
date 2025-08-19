from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/',admin.site.urls),
    path('',include('apps.core.urls')),
    path('courses/',include('apps.category_skills.urls')),
    path('register/',include('apps.accounts.urls'))
]