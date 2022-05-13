from django.urls import path
from .views import *
urlpatterns = [
    path("",home,name="home"),
    path("signin/",register,name="signin"),
    path("login/",login_user,name="login"),
    path("add/",add,name="add"),
]
