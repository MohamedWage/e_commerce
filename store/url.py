"""
URL configuration for e_commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path
from . import views


urlpatterns = [
    path('',views.ProductView.as_view(),name='home'),
    path('category/<int:category_id>/', views.CategoryDetailView.as_view(), name='category_products'),
    path('add-to-cart/<int:product_id>/',views.AddToCart.as_view(),name='addtocart'),
    path('cart',views.CartView.as_view(),name='cart'),
    path('manage-cart/<int:product_id>/<str:action>/', views.ManageCart.as_view(), name='manage_cart'),
    
]
