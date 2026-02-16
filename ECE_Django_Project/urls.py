"""ECE_Django_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ECE_Django_App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('about', views.aboutuspage),
    path('login', views.loginform),
    path('home', views.home2),
    path('add_product_page', views.add_product_page),
    path('product_search_page', views.product_search_page),
    path('modify_product_page', views.modify_product_page),


    # Logical FUnctions #
    path('register', views.user_register),
    path('userlogin', views.user_login),
    path('logout', views.logout),
    path('afterlogin', views.afterlogin_home),
    path('add_product', views.add_product),
    path('search_product', views.search_product),
    path('update/<int:id>', views.product_details_update),
    path('delete/<int:id>', views.product_details_delete),


    # for API
    path('api/products', views.add_product_api),
    path('api/products/<int:id>/', views.all_product_details),

]
