from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PrefectureListView, RoadViewSet

router = DefaultRouter()
router.register('roads', RoadViewSet, basename='road')

urlpatterns = [
    path('prefectures/', PrefectureListView.as_view(), name='prefecture-list'),
    path('', include(router.urls)),
]
