from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('home', views.home, name="home"),
    path('forms', views.forms, name="forms"),
    path('forms/sent', views.form_sent, name="form.sent"),
    path('me/<str:slug>',views.fill_form, name="forms.fill"),
    path('client/<int:pk>', views.client_details, name="client")
]
