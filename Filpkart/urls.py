"""Filpkart URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from app import views
from app.form import ChangePasswordResetForm,ChangePasswordConfirmForm


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('testing/',views.passw),

    path('signup/',views.signup,name='signup'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),

    path('profile/',views.profile,name='profile'),
    path('address/',views.address,name='address'),

    path('cart/',views.cart,name='cart'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),

    path('plus_cart',views.plus_cart),
    path('minus_cart',views.minus_cart),
    path('remove_cart',views.remove),

    path('placeorder/',views.placeorder,name='placeorder'),
    path('order_status/',views.order_status,name='order_status'),
    path('payment/',views.payment,name='payment'),

    path('product-details/<int:pk>/',views.product_details,name='product_details'),
    path('mobile/',views.mobile,name='allmobile'),
    path('mobile/<slug:data>/',views.mobile,name='mobile'),
    path('men/',views.men,name='bottomwear'),
    path('men/<slug:data>/',views.men,name='topwear'),

    path('change_password/',views.change_password,name='change_password'),

    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=ChangePasswordResetForm),name='restepassword'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=ChangePasswordConfirmForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

