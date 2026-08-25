# 交通情報マスター（全47都道府県対応）

道路交通センサスデータを都道府県ごとに検索・登録・編集・削除できるウェブアプリケーションです。
`original/` にある，Python標準のWSGI（CGI相当）とSQLiteだけで実装された旧バージョンを，
バックエンドをDjango（Django REST Framework），フロントエンドをReact（Vite）に置き換えて再構築しています。

## 構成

- `backend/` : Django + Django REST FrameworkによるAPIサーバー
- `frontend/` : React（Vite）によるSPA
- `original/` : 旧バージョン（WSGI + SQLite，参考用）
- `docs/` : 構成図などの資料

## セットアップ

### PostgreSQLの準備

DBはPostgreSQLを使います。ローカルに未導入の場合は，どちらかの方法で用意してください。

```
# Homebrewの場合
brew install postgresql@16
brew services start postgresql@16
createdb prefecture

# Dockerの場合
docker run --name prefecture-db -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres
docker exec prefecture-db createdb -U postgres prefecture
```

接続先は環境変数`POSTGRES_DB`，`POSTGRES_USER`，`POSTGRES_PASSWORD`，`POSTGRES_HOST`，
`POSTGRES_PORT`で上書きできます（`backend/config/settings.py`参照）。未設定時は
`localhost:5432`のpostgresユーザー（パスワードpostgres），DB名`prefecture`に接続します。

### バックエンド

```
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # 登録・更新・一括削除にはログインが必要

# 取得済みの都道府県を import_csv で取り込む（全47都道府県分のCSVは data/csv/ にある）
python manage.py import_csv hokkaido
python manage.py import_csv aomori
python manage.py import_csv iwate
python manage.py import_csv miyagi
python manage.py import_csv akita
python manage.py import_csv yamagata
python manage.py import_csv fukushima
python manage.py import_csv ibaraki
python manage.py import_csv tochigi
python manage.py import_csv gunma
python manage.py import_csv saitama
python manage.py import_csv chiba
python manage.py import_csv tokyo
python manage.py import_csv kanagawa
python manage.py import_csv niigata
python manage.py import_csv toyama
python manage.py import_csv ishikawa
python manage.py import_csv fukui
python manage.py import_csv yamanashi
python manage.py import_csv nagano
python manage.py import_csv gifu
python manage.py import_csv shizuoka
python manage.py import_csv aichi
python manage.py import_csv mie
python manage.py import_csv shiga
python manage.py import_csv kyoto
python manage.py import_csv osaka
python manage.py import_csv hyogo
python manage.py import_csv nara
python manage.py import_csv wakayama
python manage.py import_csv tottori
python manage.py import_csv shimane
python manage.py import_csv okayama
python manage.py import_csv hiroshima
python manage.py import_csv yamaguchi
python manage.py import_csv tokushima
python manage.py import_csv kagawa
python manage.py import_csv ehime
python manage.py import_csv kochi
python manage.py import_csv fukuoka
python manage.py import_csv saga
python manage.py import_csv nagasaki
python manage.py import_csv kumamoto
python manage.py import_csv oita
python manage.py import_csv miyazaki
python manage.py import_csv kagoshima
python manage.py import_csv okinawa

python manage.py runserver
```

`http://localhost:8000/api/` でAPIが起動します。

以前のSQLite版のデータ（`backend/db.sqlite3`）はそのまま残していますが，PostgreSQLに
切り替えた後は参照されません。PostgreSQL側は上記の`import_csv`を実行するまで空の状態です。

### フロントエンド

```
cd frontend
npm install
npm install react-router-dom
npm run dev
```

`http://localhost:5173/` でアプリにアクセスできます。

## 主な機能

- 都道府県ごとの道路データ検索（路線名，区間延長での絞り込み，任意項目でのソート）
- 路線名のオートコンプリート
- データの新規追加・更新・一括削除
- 管理画面（`/admin/`）からのデータ確認
