import csv
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from roads.models import PREFECTURE_CHOICES, Road

SUPPORTED_PREFECTURES = [code for code, _ in PREFECTURE_CHOICES]


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


class Command(BaseCommand):
    help = (
        'CSVファイルから道路データを取り込む'
        '（例: python manage.py import_csv aichi，全件は python manage.py import_csv all）'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            'prefecture',
            type=str,
            help=f'対応都道府県，または全47都道府県をまとめて取り込む\'all\': {", ".join(SUPPORTED_PREFECTURES)}',
        )
        parser.add_argument('--reset', action='store_true', help='取り込み前に既存データを削除する')

    def handle(self, *args, **options):
        prefecture = options['prefecture']
        reset = options['reset']

        if prefecture == 'all':
            for code in SUPPORTED_PREFECTURES:
                self._import_one(code, reset)
            return

        if prefecture not in SUPPORTED_PREFECTURES:
            raise CommandError(
                f"'{prefecture}' は対応していない都道府県名です。"
                f"対応都道府県: {', '.join(SUPPORTED_PREFECTURES)}（'all'で全件取り込み）"
            )

        self._import_one(prefecture, reset)

    def _import_one(self, prefecture, reset):
        csv_path = Path(settings.BASE_DIR) / 'data' / 'csv' / f'{prefecture}.csv'
        if not csv_path.exists():
            raise CommandError(f'CSVファイルが見つかりません: {csv_path}')

        if reset:
            deleted, _ = Road.objects.filter(prefecture=prefecture).delete()
            self.stdout.write(f'{prefecture}: 既存データ{deleted}件を削除しました。')

        if Road.objects.filter(prefecture=prefecture).exists():
            self.stdout.write(self.style.WARNING(
                f'{prefecture}: すでにデータが存在するため取り込みをスキップします（--resetで再取り込み可能）。'
            ))
            return

        imported = 0
        skipped = 0
        roads = []
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) < 18:
                    skipped += 1
                    continue
                try:
                    section_number = int(row[0])
                except (TypeError, ValueError):
                    skipped += 1
                    continue
                roads.append(Road(
                    prefecture=prefecture,
                    section_number=section_number,
                    route_name=row[1],
                    start_point=row[2],
                    end_point=row[3],
                    municipality_code=row[4],
                    expressway_type=row[5],
                    section_length=safe_float(row[6]),
                    upstream_point=row[7],
                    upstream_traffic=safe_int(row[8]),
                    downstream_point=row[9],
                    downstream_traffic=safe_int(row[10]),
                    total_traffic=safe_int(row[11]),
                    day_night_ratio=safe_float(row[12]),
                    congestion_degree=safe_float(row[13]),
                    upstream_speed=safe_float(row[14]),
                    downstream_speed=safe_float(row[15]),
                    road_width=safe_float(row[16]),
                    speed_limit=safe_int(row[17]),
                ))
                imported += 1

        Road.objects.bulk_create(roads, ignore_conflicts=True, batch_size=1000)
        self.stdout.write(self.style.SUCCESS(f'{prefecture}: {imported}件を取り込みました（{skipped}件スキップ）。'))
