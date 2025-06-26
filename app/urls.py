from django.urls import path,include
from .views import LoginView, ServiceCategoryViewSet, ServiceViewSet, UserProfileView,CitiznViewSet,ApartmentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'citizns', CitiznViewSet, basename='citizn')
router.register(r'apartments', ApartmentViewSet, basename='apartment')
router.register(r'service-categories', ServiceCategoryViewSet, basename='service-category')
router.register(r'services', ServiceViewSet, basename='service')
urlpatterns = [
    path("auth/token/", LoginView.as_view(), name="login"),
    path("profile/", UserProfileView.as_view(), name="user_profile"),

    path('', include(router.urls)),
]
