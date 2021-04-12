from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('home', views.home, name="home"),
    path('forms', views.forms, name="forms"),
    path('assign_forms', views.assign_forms, name="form.assign"),
    path('client/<int:pk>', views.client_details, name="client"),
    # assign_forms
]
