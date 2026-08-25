from rest_framework import pagination, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PREFECTURE_CHOICES, Road
from .serializers import RoadSerializer


class RoadPagination(pagination.PageNumberPagination):
    """道路データ一覧のページネーション（全件を一度に返さないための設定）"""

    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class RoadViewSet(viewsets.ModelViewSet):
    """道路データのCRUD・検索・一括削除・路線名一覧を提供する"""

    serializer_class = RoadSerializer
    pagination_class = RoadPagination
    # 閲覧（GET）は誰でも可，登録・更新・削除はログインユーザーのみ許可する
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Road.objects.all()
        params = self.request.query_params

        # 単一県（例: shizuoka）だけでなく，カンマ区切りで複数県（例: shizuoka,aichi）も指定できる
        prefecture = params.get('prefecture')
        if prefecture:
            prefecture_codes = [code for code in prefecture.split(',') if code]
            if prefecture_codes:
                queryset = queryset.filter(prefecture__in=prefecture_codes)

        route_name = params.get('route_name')
        if route_name and route_name != 'すべて':
            queryset = queryset.filter(route_name__icontains=route_name)

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
            prefecture_codes = [code for code in prefecture.split(',') if code]
            if prefecture_codes:
                queryset = queryset.filter(prefecture__in=prefecture_codes)
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
