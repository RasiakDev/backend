from rest_framework.routers import DefaultRouter
from eCommerce.api.urls import post_router
from django.urls import path, include
from rest_framework.authtoken import views
router = DefaultRouter()
# posts
router.registry.extend(post_router.registry)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth', views.obtain_auth_token)
]


