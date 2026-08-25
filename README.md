# 交通情報マスター（静岡・愛知・岐阜・三重）

道路交通センサスデータを都道府県ごとに検索・登録・編集・削除できるウェブアプリケーションです。
`original/` にある，Python標準のWSGI（CGI相当）とSQLiteだけで実装された旧バージョンを，
バックエンドをDjango（Django REST Framework），フロントエンドをReact（Vite）に置き換えて再構築しています。

## 構成

- `backend/` : Django + Django REST FrameworkによるAPIサーバー
- `frontend/` : React（Vite）によるSPA
- `original/` : 旧バージョン（WSGI + SQLite，参考用）
- `docs/` : 構成図などの資料

## セットアップ

### バックエンド

```
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py import_csv shizuoka
python manage.py import_csv aichi
python manage.py import_csv gifu
python manage.py import_csv mie
python manage.py runserver
```

`http://localhost:8000/api/` でAPIが起動します。

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
