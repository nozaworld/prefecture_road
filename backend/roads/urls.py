from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .auth_views import CurrentUserView, LoginView, LogoutView
from .views import PrefectureListView, RoadViewSet

router = DefaultRouter()
router.register('roads', RoadViewSet, basename='road')

urlpatterns = [
    path('prefectures/', PrefectureListView.as_view(), name='prefecture-list'),
    path('auth/me/', CurrentUserView.as_view(), name='auth-me'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutView.as_view(), name='auth-logout'),
    path('', include(router.urls)),
]
