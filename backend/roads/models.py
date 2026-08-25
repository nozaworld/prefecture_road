from django.db import models

PREFECTURE_CHOICES = [
    ('shizuoka', '静岡県'),
    ('aichi', '愛知県'),
    ('gifu', '岐阜県'),
    ('mie', '三重県'),
]


class Road(models.Model):
    """道路交通センサスの区間データ"""

    prefecture = models.CharField('都道府県', max_length=20, choices=PREFECTURE_CHOICES)
    section_number = models.IntegerField('区間番号')
    route_name = models.CharField('路線名', max_length=100)
    start_point = models.CharField('起点側路線名', max_length=200, blank=True, default='')
    end_point = models.CharField('終点側路線名', max_length=200, blank=True, default='')
    municipality_code = models.CharField('市区町村コード', max_length=20, blank=True, default='')
    expressway_type = models.CharField('専用道路', max_length=50, blank=True, default='')
    section_length = models.FloatField('区間延長(km)', default=0)
    upstream_point = models.CharField('上り観測地点', max_length=200, blank=True, default='')
    upstream_traffic = models.IntegerField('24h上り交通量(台)', default=0)
    downstream_point = models.CharField('下り観測地点', max_length=200, blank=True, default='')
    downstream_traffic = models.IntegerField('24h下り交通量(台)', default=0)
    total_traffic = models.IntegerField('24h交通量合計(台)', default=0)
    day_night_ratio = models.FloatField('昼夜率', default=0)
    congestion_degree = models.FloatField('混雑度', default=0)
    upstream_speed = models.FloatField('上り速度(km/h)', default=0)
    downstream_speed = models.FloatField('下り速度(km/h)', default=0)
    road_width = models.FloatField('幅員(m)', default=0)
    speed_limit = models.IntegerField('最高速度(km/h)', default=0)

    class Meta:
        unique_together = ('prefecture', 'section_number')
        ordering = ['section_number']
        indexes = [
            models.Index(fields=['prefecture', 'route_name']),
            models.Index(fields=['prefecture', 'section_length']),
        ]

    def __str__(self):
        return f'{self.get_prefecture_display()} {self.route_name} ({self.section_number})'
