from django.urls import path
from .views import *
urlpatterns = [
    path("",home,name="home"),
    path("signin/",register,name="signin"),
    path("login/",login_user,name="login"),
    path("logout",logout_request,name="logout_request"),
    
    path("add/",add,name="add"),
    path("my_product/",myproduct,name="my_product"),
    path("products/v=<int:pk>",products,name="products"),
    path("products/p=<int:pk>/edit",edit_product,name="product_edit"),
    

    
]
