from django.urls import path
from .views import MyTokenObtainPairView
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, CertificationViewSet, ResearchViewSet
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('certifications', CertificationViewSet,
                basename='certification')
router.register('researchs', ResearchViewSet, basename='research')
urlpatterns = router.urls

urlpatterns += [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
