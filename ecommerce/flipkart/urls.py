from django.contrib import admin
from django.urls import path,include

from .import views

from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers, serializers, viewsets


router = routers.DefaultRouter()
router.register(r'', views.RegistrationViewSet)

urlpatterns = [
    path("",views.index,name="home"),
    path("contact",views.contact,name="contact"),
    path("about",views.about,name="about"),
    path("signup",views.sign_up, name="signup"),
    path("login",views.login, name="login"),
    path("logout",views.logout, name="logout"),
    path("cart",views.cart_details, name="cart"),
    path("checkout",views.checkout, name="checkout"),
    path("order",views.order_details, name="order"),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('restapi/', include(router.urls)),


]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

