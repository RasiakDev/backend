from django.contrib import admin
from django.urls import path
from eCommerce import views
from rest_framework.routers import DefaultRouter
from ..views import PostViewSet, ProductViewSet,upload_product

post_router = DefaultRouter()
post_router.register(r'posts', PostViewSet)
post_router.register(r'products',ProductViewSet)


