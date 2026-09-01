# 交通情報マスター（全47都道府県対応）

[![CI](https://github.com/nozaworld/prefecture_road/actions/workflows/ci.yml/badge.svg)](https://github.com/nozaworld/prefecture_road/actions/workflows/ci.yml)

## 使用技術

<p style="display: inline">
  <img src="https://img.shields.io/badge/-Python-3776AB.svg?logo=python&style=for-the-badge&logoColor=white">
  <img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=for-the-badge&logoColor=white">
  <img src="https://img.shields.io/badge/-TypeScript-3178C6.svg?logo=typescript&style=for-the-badge&logoColor=white">
  <img src="https://img.shields.io/badge/-React-61DAFB.svg?logo=react&style=for-the-badge&logoColor=black">
  <img src="https://img.shields.io/badge/-PostgreSQL-4169E1.svg?logo=postgresql&style=for-the-badge&logoColor=white">
  <img src="https://img.shields.io/badge/-Docker-2496ED.svg?logo=docker&style=for-the-badge&logoColor=white">
</p>

このプロジェクトは，道路交通センサスデータを都道府県ごとに検索・登録・編集・削除できるWebアプリです．`original/`にあるPython標準のWSGI（CGI相当）とSQLiteだけで実装した旧バージョンを，バックエンドをDjango（Django REST Framework），フロントエンドをReact（Vite + TypeScript），データベースをPostgreSQLに置き換えて再構築しています．

## 概要

`original/`にある旧実装をベースに，都道府県ごとの道路区間データをRESTful APIとして扱えるようDjangoで再構築し，フロントエンドはSPAとして分離しています．検索条件の絞り込みやソート，複数県を横断した検索，路線名のオートコンプリートなど，旧バージョンにはなかった機能を追加しています．

主な機能として，以下を扱います．

- 都道府県ごとの道路区間データの検索（路線名の部分一致，区間延長の閾値指定，任意項目でのソート）
- 7地方区分でグループ化した都道府県ナビゲーションと，複数県を横断した検索（`/multi`）
- 路線名のオートコンプリート
- フロントエンド上でのログイン・ログアウト（`/login`）。ユーザー登録（サインアップ）機能は提供しない
- データの新規登録・更新・一括削除（ログインユーザーのみ）
- Django管理画面（`/admin/`）からのデータ確認
- CSVファイルからのデータ一括取り込み（管理コマンド`import_csv`，都道府県ごと，または`all`で全47都道府県まとめて）
- 一覧のページネーション（1ページ50件，`page_size`で最大200件まで変更可）

## 制約

- 対応データは全47都道府県の道路交通センサスデータに限定しており，取り込みには`backend/data/csv/`以下の都道府県別CSVファイルが必要です．
- 登録・更新・削除にはDjangoのログイン認証が必要で，サインアップ機能は実装していません（`createsuperuser`でユーザーを作成します）．
- 認証はセッション認証ベースであり，トークン認証やOAuthには対応していません．
- 複数ユーザーが同時に同じデータを編集した場合の排他制御は行っていません．

## データの出典

`backend/data/csv/`以下の道路交通データは，以下の調査によるものです．

国土交通省道路局道路調査課，全国道路・街路交通情勢調査，https://www.mlit.go.jp/road/census/r3/index.html

## 要件

バックエンド

- Python `3.11`系（DockerイメージのPythonバージョン）
- Django `4.2.30`（`requirements.txt`）
- djangorestframework `3.16.1`
- django-cors-headers `4.9.0`
- psycopg2-binary `2.9.10`
- dj-database-url `3.1.2`（本番でのDATABASE_URL対応）
- whitenoise `6.12.0`（静的ファイル配信）
- gunicorn `26.2.0`（本番用アプリケーションサーバー）
- PostgreSQL `16`

フロントエンド

- Node.js `22`系（npmはNode.jsに同梱）
- TypeScript `^6.0.3`（`devDependencies`）
- vite `^8.2.2`（`devDependencies`）
- react `^19.2.8` / react-dom `^19.2.8`
- react-router-dom `^7.18.2`
- axios `^1.19.0`
- vitest `^4.1.11`, @testing-library/react `^16.3.3`（`devDependencies`，テスト用）

起動にはDocker / Docker Composeが使える環境が必要です．

## 使い方

1. リポジトリをクローンします．

```bash
git clone https://github.com/nozaworld/prefecture_road.git
cd prefecture_road
```

2. コンテナをビルドして起動します．

```bash
docker compose up --build
```

PostgreSQL・バックエンド・フロントエンドがまとめて起動し，マイグレーションも自動で実行されます．

- API : `http://localhost:8000/api/`
- フロントエンド : `http://localhost:5173/`

3. 初回のみ，管理ユーザーの作成とCSVデータの取り込みを行います．

```bash
docker compose exec backend python manage.py createsuperuser
docker compose exec backend python manage.py import_csv all
```

停止する場合は`docker compose down`を使います．PostgreSQLのデータは名前付きボリューム（`postgres_data`）に保存されるため，`down`だけでは消えません．データごと削除する場合は`docker compose down -v`を使います．

## テスト

バックエンドは`roads/tests.py`にモデル・API・認証のテストがあります．

```bash
docker compose exec backend python manage.py test
```

フロントエンドはVitest + React Testing Libraryでコンポーネントのテストを行っています．

```bash
cd frontend
npm run test        # 一度だけ実行
npm run test:watch  # ファイル変更を監視して実行
```

pushとpull requestのたびに，GitHub Actions（`.github/workflows/ci.yml`）でバックエンドのテストと，フロントエンドのlint・テスト・ビルドを自動実行しています．

## プロジェクト構成

- `backend/config/`
  Djangoプロジェクトの設定（`settings.py`，`urls.py`，`wsgi.py`，`asgi.py`）
- `backend/roads/`
  道路データを扱うDjangoアプリ．モデル（`models.py`），APIビュー（`views.py`），シリアライザ（`serializers.py`），URLルーティング（`urls.py`），CSV取り込み用管理コマンド（`management/commands/import_csv.py`），テスト（`tests.py`）
- `backend/roads/auth_views.py`
  ログイン・ログアウト・ログイン状態確認のAPI（`/api/auth/`以下）。サインアップは提供しない
- `backend/data/csv/`
  都道府県別の道路交通センサスCSVデータ（全47都道府県分，出典は上記「データの出典」を参照）
- `frontend/src/pages/`
  `PrefecturePage.tsx`（単一県の検索・一覧・登録・編集），`MultiPrefecturePage.tsx`（複数県を横断した検索），`LoginPage.tsx`（ログイン画面）
- `frontend/src/components/`
  検索フォーム，結果テーブル，ページネーション，都道府県ナビゲーション，路線名オートコンプリートなどのUIコンポーネント（それぞれに`*.test.tsx`のテストを併置）
- `frontend/src/auth/`
  ログイン状態を管理する`AuthProvider`（`AuthContext.tsx`）と`useAuth`フック
- `frontend/src/api/client.ts`
  axiosによるバックエンドAPIクライアント（認証系のAPI呼び出しも含む）
- `frontend/src/constants/`
  都道府県一覧（`prefectures.ts`），7地方区分（`regions.ts`），検索・表示項目の定義（`roadFields.ts`）
- `original/`
  旧バージョン（Python標準WSGI + SQLite，参考用）
- `docker-compose.yml`, `backend/Dockerfile`, `frontend/Dockerfile`
  Docker Composeで一括起動するための構成（`backend/Dockerfile`は本番でもそのままgunicornで起動する）
- `frontend/vercel.json`
  Vercelにデプロイした際のSPAルーティング設定
- `.github/workflows/ci.yml`
  push・pull request時にバックエンドのテストとフロントエンドのlint・テスト・ビルドを実行するGitHub Actions

## ライセンス

このプロジェクトはMITライセンスのもとで公開されています．詳細は[LICENSE](./LICENSE)を参照してください．

## 補足

`original/`にある旧バージョンは，単一のPython標準WSGIスクリプトとSQLiteだけで完結する構成でした．本バージョンでは，APIとフロントエンドを分離し，DjangoによるCRUD機能・ログイン認証・PostgreSQLへの移行・Docker Composeでの一括起動など，旧バージョンにはなかった仕組みを追加しています．
