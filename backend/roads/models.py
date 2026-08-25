from django.db import models

# JIS都道府県コード順（全47都道府県）
PREFECTURE_CHOICES = [
    ('hokkaido', '北海道'),
    ('aomori', '青森県'),
    ('iwate', '岩手県'),
    ('miyagi', '宮城県'),
    ('akita', '秋田県'),
    ('yamagata', '山形県'),
    ('fukushima', '福島県'),
    ('ibaraki', '茨城県'),
    ('tochigi', '栃木県'),
    ('gunma', '群馬県'),
    ('saitama', '埼玉県'),
    ('chiba', '千葉県'),
    ('tokyo', '東京都'),
    ('kanagawa', '神奈川県'),
    ('niigata', '新潟県'),
    ('toyama', '富山県'),
    ('ishikawa', '石川県'),
    ('fukui', '福井県'),
    ('yamanashi', '山梨県'),
    ('nagano', '長野県'),
    ('gifu', '岐阜県'),
    ('shizuoka', '静岡県'),
    ('aichi', '愛知県'),
    ('mie', '三重県'),
    ('shiga', '滋賀県'),
    ('kyoto', '京都府'),
    ('osaka', '大阪府'),
    ('hyogo', '兵庫県'),
    ('nara', '奈良県'),
    ('wakayama', '和歌山県'),
    ('tottori', '鳥取県'),
    ('shimane', '島根県'),
    ('okayama', '岡山県'),
    ('hiroshima', '広島県'),
    ('yamaguchi', '山口県'),
    ('tokushima', '徳島県'),
    ('kagawa', '香川県'),
    ('ehime', '愛媛県'),
    ('kochi', '高知県'),
    ('fukuoka', '福岡県'),
    ('saga', '佐賀県'),
    ('nagasaki', '長崎県'),
    ('kumamoto', '熊本県'),
    ('oita', '大分県'),
    ('miyazaki', '宮崎県'),
    ('kagoshima', '鹿児島県'),
    ('okinawa', '沖縄県'),
]


class Road(models.Model):
    """道路交通センサスの区間データ"""

    prefecture = models.CharField('都道府県', max_length=20, choices=PREFECTURE_CHOICES)
    section_number = models.BigIntegerField('区間番号')
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
