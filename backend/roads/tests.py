from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Road


class RoadModelTests(TestCase):
    """モデル単体の振る舞いを確認する"""

    def test_str_includes_prefecture_display_and_route_name(self):
        road = Road.objects.create(
            prefecture='shizuoka',
            section_number=1,
            route_name='国道1号',
        )
        self.assertIn('静岡県', str(road))
        self.assertIn('国道1号', str(road))

    def test_unique_together_prevents_duplicate_section(self):
        Road.objects.create(prefecture='shizuoka', section_number=1, route_name='国道1号')
        with self.assertRaises(Exception):
            Road.objects.create(prefecture='shizuoka', section_number=1, route_name='別の路線')


class PrefectureListApiTests(TestCase):
    """都道府県一覧APIの確認"""

    def setUp(self):
        self.client = APIClient()

    def test_prefecture_list_is_public_and_includes_registered_prefectures(self):
        response = self.client.get('/api/prefectures/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        codes = [item['code'] for item in response.data]
        for expected in ('shizuoka', 'aichi', 'gifu', 'mie', 'nagano',
                          'niigata', 'toyama', 'ishikawa', 'fukui', 'yamanashi'):
            self.assertIn(expected, codes)


class RoadApiTests(TestCase):
    """道路データAPIの検索・権限まわりの確認"""

    def setUp(self):
        self.client = APIClient()
        self.road = Road.objects.create(
            prefecture='shizuoka', section_number=1, route_name='国道1号',
        )
        self.user = User.objects.create_user(username='tester', password='testpass123')

    def test_road_list_is_public(self):
        response = self.client.get('/api/roads/', {'prefecture': 'shizuoka'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_road_list_can_filter_by_prefecture(self):
        Road.objects.create(prefecture='nagano', section_number=1, route_name='国道19号')
        response = self.client.get('/api/roads/', {'prefecture': 'nagano'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['route_name'], '国道19号')

    def test_route_name_search_is_partial_match(self):
        Road.objects.create(prefecture='shizuoka', section_number=2, route_name='中央自動車道西宮線')
        response = self.client.get('/api/roads/', {'route_name': '西宮線'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_route_name_search_ignores_case(self):
        Road.objects.create(prefecture='shizuoka', section_number=2, route_name='Route ABC')
        response = self.client.get('/api/roads/', {'route_name': 'abc'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_route_name_zenbu_returns_all(self):
        Road.objects.create(prefecture='shizuoka', section_number=2, route_name='国道2号')
        response = self.client.get('/api/roads/', {'route_name': 'すべて'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_anonymous_cannot_create_road(self):
        response = self.client.post('/api/roads/', {
            'prefecture': 'shizuoka',
            'section_number': 2,
            'route_name': '国道2号',
        })
        self.assertIn(response.status_code,
                       (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.assertEqual(Road.objects.count(), 1)

    def test_authenticated_user_can_create_road(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/roads/', {
            'prefecture': 'shizuoka',
            'section_number': 2,
            'route_name': '国道2号',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Road.objects.count(), 2)

    def test_anonymous_cannot_update_road(self):
        response = self.client.patch(f'/api/roads/{self.road.id}/', {'route_name': '改変済み'})
        self.assertIn(response.status_code,
                       (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.road.refresh_from_db()
        self.assertEqual(self.road.route_name, '国道1号')

    def test_anonymous_cannot_bulk_delete(self):
        response = self.client.post('/api/roads/bulk_delete/', {'ids': [self.road.id]})
        self.assertIn(response.status_code,
                       (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        self.assertEqual(Road.objects.count(), 1)

    def test_authenticated_user_can_bulk_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/roads/bulk_delete/', {'ids': [self.road.id]})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['deleted'], 1)
        self.assertEqual(Road.objects.count(), 0)
