
import forms_builder.forms.urls
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('food.urls')),
    path('forms/', include(forms_builder.forms.urls)),
]
