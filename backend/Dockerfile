FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 本番向けの静的ファイル（管理画面・DRF Browsable APIのCSS/JSなど）をビルド時にまとめておく。
# DEBUG=Trueがデフォルトのため，ビルド時に環境変数を渡さなくても実行できる。
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# デフォルトはgunicornでの本番起動。ローカル開発でのDocker Composeでは
# docker-compose.ymlのcommandでmigrate + runserverに上書きしている。
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
