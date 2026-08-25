from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PREFECTURE_CHOICES, Road
from .serializers import RoadSerializer


class RoadViewSet(viewsets.ModelViewSet):
    """道路データのCRUD・検索・一括削除・路線名一覧を提供する"""

    serializer_class = RoadSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Road.objects.all()
        params = self.request.query_params

        prefecture = params.get('prefecture')
        if prefecture:
            queryset = queryset.filter(prefecture=prefecture)

        route_name = params.get('route_name')
        if route_name and route_name != 'すべて':
            queryset = queryset.filter(route_name=route_name)

        length_value = params.get('length_value')
        length_op = params.get('length_op')
        if length_value:
            try:
                value = float(length_value)
                if length_op == 'lte':
                    queryset = queryset.filter(section_length__lte=value)
                else:
                    queryset = queryset.filter(section_length__gte=value)
            except (TypeError, ValueError):
                pass

        sort_column = params.get('sort_column')
        sort_order = params.get('sort_order', 'ASC')
        allowed_sort_fields = {f.name for f in Road._meta.get_fields()}
        if sort_column and sort_column in allowed_sort_fields:
            prefix = '-' if sort_order == 'DESC' else ''
            queryset = queryset.order_by(f'{prefix}{sort_column}', 'section_number')

        return queryset

    @action(detail=False, methods=['get'])
    def route_names(self, request):
        """オートコンプリート用の路線名一覧"""
        prefecture = request.query_params.get('prefecture')
        queryset = Road.objects.all()
        if prefecture:
            queryset = queryset.filter(prefecture=prefecture)
        names = list(
            queryset.order_by('route_name').values_list('route_name', flat=True).distinct()
        )
        return Response(names)

    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        """チェックボックスで選択した区間の一括削除"""
        ids = request.data.get('ids', [])
        deleted_count, _ = Road.objects.filter(id__in=ids).delete()
        return Response({'deleted': deleted_count}, status=status.HTTP_200_OK)


class PrefectureListView(APIView):
    """対応都道府県の一覧（ナビゲーションメニュー用）"""

    def get(self, request):
        return Response([{'code': code, 'name': name} for code, name in PREFECTURE_CHOICES])
