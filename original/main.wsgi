#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Python 3.9.22
import sys
import os
import re
import textwrap
from urllib.parse import parse_qs
import cgitb
cgitb.enable()
import sqlite3
import csv
import secrets
import html
import json

# クラス定義
class Prefecture:
    """都道府県情報クラス"""
    name: str
    csv_file: str
    db_file: str
    name_jp: str
    
    def __init__(self, name: str):
        self.name = name
        self.csv_file = 'csv/' + name + '.csv'
        self.db_file = 'db/' + name + '.db'

    def edit_name(self, new_name: str) -> None:
        """都道府県名を変更"""
        self.name = new_name
        self.name_jp = dict_en2jp[new_name]
        self.csv_file = 'csv/' + new_name + '.csv'
        self.db_file = 'db/' + new_name + '.db'

# グローバル変数群
LOCALHOST: bool = True
APP_DIR: str = os.path.dirname(os.path.abspath(__file__)) 
CSRF_TOKENS: dict[str, bool] = {}
CSRF_TOKEN_LENGTH: int = 32
ROWNAME_FRONT_TO_BACK: dict[str, str] = { #フロントエンドの選択とDBカラム名の対応
        "路線名":"路線名",
        "起点側路線名":"起点側",
        "終点側路線名":"終点側",
        "市区町村コード":"市区町村コード",
        "専用道路":"自動車専用道路の別",
        "区間延長(km)":"区間延長",
        "上り観測地点":"上り地点地名",
        "24h上り交通量(台)":"上り交通量",
        "下り観測地点":"下り地点地名",
        "24h下り交通量(台)":"下り交通量",
        "24h交通量合計(台)":"交通量合計",
        "昼夜率":"昼夜率",
        "混雑度":"混雑度",
        "上り速度(km/h)":"上り旅行速度",
        "下り速度(km/h)":"下り旅行速度",
        "幅員(m)":"道路部幅員",
        "最高速度(km/h)":"指定最高速度"
    }

dict_en2jp: dict[str, str] = { # 都道府県情報（csv追加時に変更する）
        "shizuoka": "静岡県",
        "aichi": "愛知県",
        "gifu": "岐阜県",
        "mie": "三重県"
}
supported_prefectures: list[str] = list(dict_en2jp.keys())
supported_prefectures_jp: list[str] = list(dict_en2jp.values())

PREFECTURE: Prefecture = Prefecture(name="") # プログラム本文で使う都道府県情報のインスタンスの初期化

def generate_csrf_token() -> str:
    """CSRFトークンを生成"""
    # 乱数生成
    token = secrets.token_hex(CSRF_TOKEN_LENGTH)
    CSRF_TOKENS[token] = True
    return token

def validate_csrf_token(token: str) -> bool:
    """CSRFトークンを検証"""
    # リストに存在するか否か
    return token in CSRF_TOKENS

def createTable() -> None:
    """roadsテーブルを作成"""
    con = sqlite3.connect(PREFECTURE.db_file)
    cur = con.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS roads (
            区間番号 INTEGER PRIMARY KEY,
            路線名 TEXT,
            起点側 TEXT,
            終点側 TEXT,
            市区町村コード TEXT,
            自動車専用道路の別 TEXT,
            区間延長 REAL,
            上り地点地名 TEXT,
            上り交通量 INTEGER,
            下り地点地名 TEXT,
            下り交通量 INTEGER,
            交通量合計 INTEGER,
            昼夜率 REAL,
            混雑度 REAL,
            上り旅行速度 REAL,
            下り旅行速度 REAL,
            道路部幅員 REAL,
            指定最高速度 INTEGER
        )
    ''')
    # インデックス作成
    cur.execute('CREATE INDEX IF NOT EXISTS idx_route_name ON roads(路線名)')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_length ON roads(区間延長)')
    con.commit()
    cur.close()
    con.close()

def importCSV() -> None:
    """csvをインポート"""
    csv_path = os.path.join(APP_DIR, PREFECTURE.csv_file)
    # CSVファイルが存在しない場合は終了
    if not os.path.exists(csv_path):
        print(f"CSV file not found: {html.escape(csv_path)}", file=sys.stderr)
        return

    con = sqlite3.connect(PREFECTURE.db_file)
    cur = con.cursor()
    cur.execute('SELECT COUNT(*) FROM roads')
    count = cur.fetchone()[0]
    # データがすでに存在する場合はスキップ
    if count > 0:
        cur.close()
        con.close()
        print("Data already imported, skipping CSV import.", file=sys.stderr)
        return

    imported = 0
    # CSVファイルを読み込み、データを挿入
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) 
        for row in reader:
            if len(row) >= 18:
                try:
                    # データ挿入
                    cur.execute('''
                        INSERT INTO roads VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''', tuple(row[:18]))
                    imported += 1
                except sqlite3.Error as e:
                    print(f"Error importing row: {html.escape(str(e))}", file=sys.stderr)
                    print(f"Skipping row: {html.escape(str(row))}", file=sys.stderr)
    
    con.commit()
    cur.close()
    con.close()

def getRouteNames() -> list[str]:
    """路線名の一覧を取得"""
    con = sqlite3.connect(PREFECTURE.db_file)
    cur = con.cursor()
    cur.execute('SELECT DISTINCT 路線名 FROM roads ORDER BY 路線名')
    routes = [r[0] for r in cur.fetchall()]
    cur.close()
    con.close()
    return routes

def searchRoads(route_name: str, length_value: float = None, length_op: str = None, sort_column: str = None, sort_order: str = None) -> list[tuple]:
    """道路データを検索"""
    con = sqlite3.connect(PREFECTURE.db_file)
    cur = con.cursor()
    # 全件検索時
    if route_name == "すべて":
        sql = 'SELECT * FROM roads WHERE 1=1'
        params = []
    # 特定路線名検索時
    else:
        sql = 'SELECT * FROM roads WHERE 路線名 = ?'
        params = [route_name]
    # 区間延長フィルタ
    if length_value and length_op:
        try:
            length_val = float(length_value)
            if length_op == 'gte':
                sql += ' AND 区間延長 >= ?'
            elif length_op == 'lte':
                sql += ' AND 区間延長 <= ?'
            else:
                raise ValueError("Invalid length_op")
            params.append(length_val)
        except (ValueError, TypeError) as e:
            print(f"Error in length filter: {html.escape(str(e))}", file=sys.stderr)
    # ソート処理
    if sort_order not in ['ASC', 'DESC']:
        sort_order = 'ASC'
    
    if sort_column and sort_column in ROWNAME_FRONT_TO_BACK:
        sql += f' ORDER BY {ROWNAME_FRONT_TO_BACK[sort_column]} {sort_order}, 区間番号 ASC'
    else:
        sql += ' ORDER BY 区間番号 ASC'
    # sql文の組み立てと実行
    cur.execute(sql, params)
    roads = cur.fetchall()
    cur.close()
    con.close()
    
    return roads

def getRoadByKukanNo(kukan_no: str):
    """区間番号で道路データを1件取得"""
    con = sqlite3.connect(PREFECTURE.db_file)
    cur = con.cursor()
    try:
        cur.execute('SELECT * FROM roads WHERE 区間番号 = ?', (kukan_no,))
        road = cur.fetchone()
    except sqlite3.Error as e:
        print(f"Error getting road: {html.escape(str(e))}", file=sys.stderr)
        road = None
    finally:
        cur.close()
        con.close()
    return road

def addRoad(data: tuple) -> bool:
    """道路データを追加"""
    con = sqlite3.connect(PREFECTURE.db_file)
    cur = con.cursor()
    try:
        cur.execute('''
            INSERT INTO roads VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', data)
        con.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False
    except Exception as e:
        print(f"Error adding road: {e}", file=sys.stderr)
        success = False
    finally:
        cur.close()
        con.close()
    return success

def updateRoad(kukan_no: str, data: tuple) -> bool:
    """道路データを更新"""
    con = sqlite3.connect(PREFECTURE.db_file)
    cur = con.cursor()
    try:
        cur.execute('''
            UPDATE roads SET
                路線名 = ?,
                起点側 = ?,
                終点側 = ?,
                市区町村コード = ?,
                自動車専用道路の別 = ?,
                区間延長 = ?,
                上り地点地名 = ?,
                上り交通量 = ?,
                下り地点地名 = ?,
                下り交通量 = ?,
                交通量合計 = ?,
                昼夜率 = ?,
                混雑度 = ?,
                上り旅行速度 = ?,
                下り旅行速度 = ?,
                道路部幅員 = ?,
                指定最高速度 = ?
            WHERE 区間番号 = ?
        ''', (*data[1:], kukan_no))
        con.commit()
        success = cur.rowcount > 0
    except Exception as e:
        print(f"Error updating road: {e}", file=sys.stderr)
        success = False
    finally:
        cur.close()
        con.close()
    return success

def deleteRoads(kukan_nos: list[str]) -> None:
    """道路データを一括削除"""
    con = sqlite3.connect(PREFECTURE.db_file)
    cur = con.cursor()
    for kukan_no in kukan_nos:
        cur.execute('DELETE FROM roads WHERE 区間番号 = ?', (kukan_no,))
    con.commit()
    cur.close()
    con.close()

def serveFile(environ: dict, start_response: callable) -> list[bytes]:
    """CSSファイルなどを送信"""
    allowed_types = {'.css': 'text/css', '.js': 'application/javascript'}
    path = environ.get('PATH_INFO', '')
    if not re.match(r'^/static/', path):
        start_response('403 Forbidden', [
            ('Content-Type', 'text/plain'),
            ('X-Frame-Options', 'DENY')
        ])
        return [b"Forbidden."]

    # パスを安全に結合して正規化
    requested_path = os.path.normpath(os.path.join(APP_DIR, path.lstrip('/')))
    static_root = os.path.join(APP_DIR, 'static')

    if not requested_path.startswith(static_root):
        start_response('403 Forbidden', [
            ('Content-Type', 'text/plain'),
            ('X-Frame-Options', 'DENY')
        ])
        return [b"Access denied."]

    ext = os.path.splitext(requested_path)[1].lower()
    content_type = allowed_types.get(ext)

    if not (os.path.isfile(requested_path) and content_type):
        start_response('404 Not Found', [
            ('Content-Type', 'text/plain'),
            ('X-Frame-Options', 'DENY')
        ])
        return [b"Not found."]

    try:
        with open(requested_path, "rb") as f:
            data = f.read()
    except OSError as e:
        print(f"File read error: {e}", file=sys.stderr)
        start_response('500 Internal Server Error', [
            ('Content-Type', 'text/plain'),
            ('X-Frame-Options', 'DENY')
        ])
        return [b"Internal server error"]

    headers = [
        ('Content-Type', content_type),
        ('Content-Length', str(len(data))),
        ('X-Frame-Options', 'DENY'),
        ('Cache-Control', 'public, max-age=3600')
    ]
    start_response('200 OK', headers)
    return [data]

def parse_request_application(environ: dict) -> tuple[str, dict, bool]:
    """リクエストを解析"""
    request_method = environ.get('REQUEST_METHOD', 'GET')
    form = {}
    valid_csrf = True
    
    if request_method == 'POST':
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
        except ValueError:
            content_length = 0
            print("Invalid CONTENT_LENGTH", file=sys.stderr)

        if content_length > 0:
            request_body = environ['wsgi.input'].read(content_length).decode('utf-8')
            form = parse_qs(request_body)

        token = form.get('csrf_token', [''])[0] if form else ''
        if not validate_csrf_token(token):
            valid_csrf = False
        else:
            try:
                CSRF_TOKENS.pop(token, None)
            except Exception:
                print("Error removing CSRF token", file=sys.stderr)
    
    return request_method, form, valid_csrf

def process_delete_application(form: dict) -> str:
    """一括削除処理"""
    delete_ids = form.get('delete_checkbox', [])
    route_name = form.get("route_name", [""])[0]
    if delete_ids:
        deleteRoads(delete_ids)
        return f"「{route_name}」について，{len(delete_ids)}件のデータを削除しました。"
    else:
        return "削除する項目を選択してください。"

def process_add_application(form: dict) -> str:
    """新規追加処理"""
    try:
        def get_float(key: str, default=None):
            val = form.get(key, [""])[0]
            if val == "" or val is None:
                return default
            try:
                return float(val)
            except ValueError:
                print(f"Error converting {html.escape(key)} to float: {html.escape(val)}", file=sys.stderr)
                return default

        def get_int(key: str, default=None):
            val = form.get(key, [""])[0]
            if val == "" or val is None:
                return default
            try:
                return int(val)
            except ValueError:
                print(f"Error converting {html.escape(key)} to int: {html.escape(val)}", file=sys.stderr)
                return default
        
        data = [
            form.get("区間番号", [""])[0],
            form.get("路線名", [""])[0],
            form.get("起点側", [""])[0],
            form.get("終点側", [""])[0],
            form.get("市区町村コード", [""])[0],
            form.get("自動車専用道路の別", [""])[0],
            get_float("区間延長", 0.0),
            form.get("上り地点地名", [""])[0],
            get_int("上り交通量", 0),
            form.get("下り地点地名", [""])[0],
            get_int("下り交通量", 0),
            get_int("交通量合計", 0),
            get_float("昼夜率", 0.0),
            get_float("混雑度", 0.0),
            get_float("上り旅行速度", 0.0),
            get_float("下り旅行速度", 0.0),
            get_float("道路部幅員", 0.0),
            get_int("指定最高速度", 0)
        ]

        if not data[0] or not data[1] or not data[0].strip() or not data[1].strip():
            return "区間番号と路線名は必須です。"
        elif addRoad(data):
            return "データを追加しました。"
        else:
            return "データの追加に失敗しました（区間番号が重複している可能性があります）。"
    except Exception as e:
        print(f"Error in add form: {html.escape(str(e))}", file=sys.stderr)
        return "データの追加に失敗しました: 入力値を確認してください。"

def process_update_application(form: dict) -> str:
    """更新処理"""
    try:
        def get_float(key: str, default=None):
            val = form.get(key, [""])[0]
            if val == "" or val is None:
                return default
            try:
                return float(val)
            except ValueError:
                print(f"Error converting {html.escape(key)} to float: {html.escape(val)}", file=sys.stderr)
                return default

        def get_int(key: str, default=None):
            val = form.get(key, [""])[0]
            if val == "" or val is None:
                return default
            try:
                return int(val)
            except ValueError:
                print(f"Error converting {html.escape(key)} to int: {html.escape(val)}", file=sys.stderr)
                return default
        
        kukan_no = form.get("区間番号", [""])[0]
        
        data = [
            kukan_no,
            form.get("路線名", [""])[0],
            form.get("起点側", [""])[0],
            form.get("終点側", [""])[0],
            form.get("市区町村コード", [""])[0],
            form.get("自動車専用道路の別", [""])[0],
            get_float("区間延長", 0.0),
            form.get("上り地点地名", [""])[0],
            get_int("上り交通量", 0),
            form.get("下り地点地名", [""])[0],
            get_int("下り交通量", 0),
            get_int("交通量合計", 0),
            get_float("昼夜率", 0.0),
            get_float("混雑度", 0.0),
            get_float("上り旅行速度", 0.0),
            get_float("下り旅行速度", 0.0),
            get_float("道路部幅員", 0.0),
            get_int("指定最高速度", 0)
        ]

        if not kukan_no or not data[1]:
            return "区間番号と路線名は必須です。"
        elif updateRoad(kukan_no, data):
            return f"区間番号 {kukan_no} のデータを更新しました。"
        else:
            return "データの更新に失敗しました。"
    except Exception as e:
        print(f"Error in update form: {html.escape(str(e))}", file=sys.stderr)
        return "データの更新に失敗しました: 入力値を確認してください。"

def process_search_application(form: dict) -> tuple[list[tuple], str, str, str, str, str, str]:
    """検索処理"""
    route_name = form.get("route_name", [""])[0]
    length_value = form.get("length_value", [""])[0]
    length_op = form.get("length_op", [""])[0]
    sort_column = form.get("sort_column", [""])[0]
    sort_order = form.get("sort_order", ["ASC"])[0]
    
    roads_to_display = []
    msg = ""

    sanitized_length_value = length_value
    if sanitized_length_value:
            try:
                val = float(length_value)
                if val < 0:
                    val = 0.0
                sanitized_length_value = str(val)
            except ValueError:
                sanitized_length_value = ""
    if not (route_name in ["すべて"] + getRouteNames()):
        msg = "無効な路線名が選択されました。"
    elif route_name:
        roads_to_display = searchRoads(route_name, sanitized_length_value, length_op, sort_column, sort_order)
        
        if route_name == "すべて":
            msg = "「すべて」の路線の"
        else:
            msg = f"「{route_name}」の"
        
        if length_value:
            if length_op == "lte":
                msg += f"区間延長が「{sanitized_length_value} km以下」の"
            else:
                msg += f"区間延長が「{sanitized_length_value} km以上」の"
        if sort_column:
            if sort_order == "DESC":
                msg += f"降順ソート {sort_column} の"
            else:
                msg += f"昇順ソート {sort_column} の"
        msg += f"検索結果: {len(roads_to_display)}件"
    else:
        msg = "路線名を選択してください。"
    
    return roads_to_display, msg, route_name, sanitized_length_value, length_op, sort_column, sort_order

def build_form_options_application(selected_route: str, length_op: str, sort_column: str, sort_order: str) -> dict:
    """フォームのオプション要素を構築"""
    route_names = getRouteNames()
    route_options = ["すべて"] + route_names

    row_names = ["路線名","起点側路線名","終点側路線名","市区町村コード","専用道路","区間延長(km)","上り観測地点","24h上り交通量(台)","下り観測地点","24h下り交通量(台)","24h交通量合計(台)","昼夜率","混雑度","上り速度(km/h)","下り速度(km/h)","幅員(m)","最高速度(km/h)"]
    sort_options = "".join(
        f'<option value="{html.escape(r)}"{" selected" if r == sort_column else ""}>{html.escape(r)}</option>'
        for r in row_names
    )

    glte_lists = ["gte", "lte"]
    glte_options = "".join(
        f'<option value="{op}"{" selected" if op == length_op else ""}>{"以上" if op == "gte" else "以下"}</option>'
        for op in glte_lists
    )

    adesc_lists = ["ASC", "DESC"]
    adesc_options = "".join(
        f'<option value="{op}"{" selected" if op == sort_order else ""}>{ "昇順" if op == "ASC" else "降順" }</option>'
        for op in adesc_lists
    )

    return {
        'route_options': route_options,
        'sort_options': sort_options,
        'glte_options': glte_options,
        'adesc_options': adesc_options
    }

def build_update_form_html(road_data: tuple, csrf_token: str) -> str:
    """更新フォームHTMLを構築"""
    return f'''
    <div class="update-section">
        <h3>データ更新（区間番号: {html.escape(str(road_data[0]))}）</h3>
        <form class="update-form" method="POST" action="/">
            <input type="hidden" name="csrf_token" value="{csrf_token}">
            <input type="hidden" name="区間番号" value="{html.escape(str(road_data[0]))}">
            <input type="text" name="路線名" placeholder="路線名*" value="{html.escape(str(road_data[1]))}" required>
            <input type="text" name="起点側" placeholder="起点側" value="{html.escape(str(road_data[2]))}">
            <input type="text" name="終点側" placeholder="終点側" value="{html.escape(str(road_data[3]))}">
            <input type="text" name="市区町村コード" placeholder="市区町村コード" value="{html.escape(str(road_data[4]))}">
            <input type="text" name="自動車専用道路の別" placeholder="自動車専用道路の別" value="{html.escape(str(road_data[5]))}">
            <input type="number" name="区間延長" placeholder="区間延長" step="0.01" value="{road_data[6] if road_data[6] else ''}">
            <input type="text" name="上り地点地名" placeholder="上り地点地名" value="{html.escape(str(road_data[7]))}">
            <input type="number" name="上り交通量" placeholder="上り交通量" value="{road_data[8] if road_data[8] else ''}">
            <input type="text" name="下り地点地名" placeholder="下り地点地名" value="{html.escape(str(road_data[9]))}">
            <input type="number" name="下り交通量" placeholder="下り交通量" value="{road_data[10] if road_data[10] else ''}">
            <input type="number" name="交通量合計" placeholder="交通量合計" value="{road_data[11] if road_data[11] else ''}">
            <input type="number" name="昼夜率" placeholder="昼夜率" step="0.01" value="{road_data[12] if road_data[12] else ''}">
            <input type="number" name="混雑度" placeholder="混雑度" step="0.01" value="{road_data[13] if road_data[13] else ''}">
            <input type="number" name="上り旅行速度" placeholder="上り旅行速度" step="0.01" value="{road_data[14] if road_data[14] else ''}">
            <input type="number" name="下り旅行速度" placeholder="下り旅行速度" step="0.01" value="{road_data[15] if road_data[15] else ''}">
            <input type="number" name="道路部幅員" placeholder="道路部幅員" step="0.01" value="{road_data[16] if road_data[16] else ''}">
            <input type="number" name="指定最高速度" placeholder="指定最高速度" value="{road_data[17] if road_data[17] else ''}">
            <div class="button-group">
                <button type="submit" name="update" value="1">更新実行</button>
                <button type="submit" name="cancel_update" value="1">キャンセル</button>
            </div>
        </form>
    </div>
    '''

def build_html_application(msg: str, roads_to_display: list[tuple], csrf_token_local: str, options: dict, length_value: str, length_op: str, edit_mode: bool = False, edit_kukan_no: str = None) -> str:
    """HTML全体を構築"""
    css_code = textwrap.dedent('''
    <link rel="stylesheet" type="text/css" href="/static/default.css">
    ''')
    js_code = textwrap.dedent(f'''
    <script defer>
        const routeNames = {json.dumps(options["route_options"], ensure_ascii=False)};
    </script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="/static/default.js" defer charset="utf-8"></script>
    ''')
    hcontent = textwrap.dedent(f'''
    <div class="hamburger">
        <span></span>
        <span></span>
        <span></span>
    </div>
  <nav class="menu">
    <ul>
    ''')
    for pref in supported_prefectures:
        hcontent += f'<li><a href="{pref}">{dict_en2jp[pref]}の道路</a></li>\n'
    hcontent += '</ul>\n</nav>\n'

    tmpl = textwrap.dedent('''
    <html lang="ja">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="author" content="N.Mitsuki">
    <meta name="description" content="{PREF}の交通情報を提供するウェブアプリケーションです。">
    <title>交通情報マスター（{PREF}の道路）</title>
    {css}
    </head>
    {hamburger}
    {body}
    {js}
    </html>
    ''')
    # print(json.dumps(options["route_options"], ensure_ascii=False))
    search_form = f'''
    <div class="search-section">
        <h3>検索条件</h3>
        <form class="search-form" method="POST" action="/" id="mainForm">
            <input type="hidden" name="csrf_token" value="{csrf_token_local}">
            <input type="hidden" name="route_name" required>
            <div id="search-form1">
                <label for="routeInput">路線名（必須）:</label>
                <div class="input-wrapper">
                    <input type="text" id="routeInput" placeholder="例: 東名" autocomplete="off" value="">
                    <ul id="suggestions"></ul>
                </div>
            </div>
            <div id ="search-form2">
                <label>区間延長（km）:</label>
                <input type="number" name="length_value" step="0.01" placeholder="数値を入力" value="{html.escape(length_value)}">
                <select name="length_op"">
                    {options['glte_options']}
                </select>
            </div>
            <div id ="search-form2">
                <label>ソート項目:</label>
                <select name="sort_column" class="sort-column">
                    <option value="">選択してください</option>
                    {options['sort_options']}
                </select>
                <select name="sort_order">
                    {options['adesc_options']}
                </select>
            </div>
            <div id ="search-button">
                <input type="submit" name="search" value="検索">
                <button type="submit" name="bulk_delete" value="1" onclick="return confirm('選択した項目を削除しますか？');">削除</button>
            </div>
        </form>
    </div>
    '''

    add_form = f'''
    <div class="add-section">
        <h3>新規データ追加</h3>
        <form class="add-form" method="POST" action="/">
            <input type="hidden" name="csrf_token" value="{csrf_token_local}">
            <input type="number" name="区間番号" placeholder="区間番号*" required>
            <input type="text" name="路線名" placeholder="路線名*" required>
            <input type="text" name="起点側" placeholder="起点側">
            <input type="text" name="終点側" placeholder="終点側">
            <input type="text" name="市区町村コード" placeholder="市区町村コード">
            <input type="text" name="自動車専用道路の別" placeholder="自動車専用道路の別">
            <input type="number" name="区間延長" placeholder="区間延長" step="0.01">
            <input type="text" name="上り地点地名" placeholder="上り地点地名">
            <input type="number" name="上り交通量" placeholder="上り交通量">
            <input type="text" name="下り地点地名" placeholder="下り地点地名">
            <input type="number" name="下り交通量" placeholder="下り交通量">
            <input type="number" name="交通量合計" placeholder="交通量合計">
            <input type="number" name="昼夜率" placeholder="昼夜率" step="0.01">
            <input type="number" name="混雑度" placeholder="混雑度" step="0.01">
            <input type="number" name="上り旅行速度" placeholder="上り旅行速度" step="0.01">
            <input type="number" name="下り旅行速度" placeholder="下り旅行速度" step="0.01">
            <input type="number" name="道路部幅員" placeholder="道路部幅員" step="0.01">
            <input type="number" name="指定最高速度" placeholder="指定最高速度">
            <button type="submit" name="add" value="1">追加</button>
        </form>
    </div>
    '''

    # 更新フォーム表示
    update_form_html = ""
    if edit_mode and edit_kukan_no:
        road_data = getRoadByKukanNo(edit_kukan_no)
        if road_data:
            update_form_html = build_update_form_html(road_data, csrf_token_local)

    grid_rows = ""
    for idx, road in enumerate(roads_to_display, 1):
        grid_rows += f'''
        <tr>
            <td>{idx}</td>
            <td>{html.escape(str(road[1]))}</td>
            <td>{html.escape(str(road[2]))}</td>
            <td>{html.escape(str(road[3]))}</td>
            <td>{html.escape(str(road[4]))}</td>
            <td>{html.escape(str(road[5]))}</td>
            <td>{road[6]}</td>
            <td>{html.escape(str(road[7]))}</td>
            <td>{road[8]}</td>
            <td>{html.escape(str(road[9]))}</td>
            <td>{road[10]}</td>
            <td>{road[11]}</td>
            <td>{road[12]}</td>
            <td>{road[13]}</td>
            <td>{road[14]}</td>
            <td>{road[15]}</td>
            <td>{road[16]}</td>
            <td>{road[17]}</td>
            <td><input type="checkbox" name="delete_checkbox" value="{html.escape(str(road[0]))}" form="mainForm"></td>
            <td>
                <form method="POST" action="/" style="display:inline;">
                    <input type="hidden" name="csrf_token" value="{csrf_token_local}">
                    <input type="hidden" name="edit_kukan_no" value="{html.escape(str(road[0]))}">
                    <button type="submit" name="edit" value="1" class="edit-btn">編集</button>
                </form>
            </td>
        </tr>
        '''

    grid_table = f'''
    <div class="grid-section">
        <table>
            <thead>
                <tr>
                    <th>No</th>
                    <th>路線名</th>
                    <th>起点側路線名</th>
                    <th>終点側路線名</th>
                    <th>市区町村コード</th>
                    <th>専用道路</th>
                    <th>区間延長(km)</th>
                    <th>上り観測地点</th>
                    <th>24h上り交通量(台)</th>
                    <th>下り観測地点</th>
                    <th>24h下り交通量(台)</th>
                    <th>24h交通量合計(台)</th>
                    <th>昼夜率</th>
                    <th>混雑度</th>
                    <th>上り速度(km/h)</th>
                    <th>下り速度(km/h)</th>
                    <th>幅員(m)</th>
                    <th>最高速度(km/h)</th>
                    <th>選択</th>
                    <th>編集</th>
                </tr>
            </thead>
            <tbody>
                {grid_rows if grid_rows else '<tr><td colspan="20">検索結果がありません</td></tr>'}
            </tbody>
        </table>
    </div>
    '''
    
    msg_html = f'<div class="message">{html.escape(msg)}</div>' if msg else ''
    
    bcontent = f'''
    <body>
        <header>
        交通情報マスター（{PREFECTURE.name_jp}の道路）</header>
        <div class="spacer1"></div>
        {search_form}
        <div class="spacer2"></div>
        {msg_html}
        {grid_table}
        {update_form_html}
        {add_form}
    </body>
    '''

    return tmpl.format(PREF=PREFECTURE.name_jp, css=css_code, hamburger=hcontent, body=bcontent, js=js_code)

def url_with_prefecture_application(environ: dict) -> None:
    """URLから都道府県名を取得して設定"""
    path = environ.get('PATH_INFO', '')
    prefecture = path.split('/')[-1]
    if str(prefecture) in supported_prefectures:
        PREFECTURE.edit_name(str(prefecture))
        createTable()
        importCSV()

def application(environ: dict, start_response: callable) -> list[bytes]:
    """アプリケーション本体"""
    if LOCALHOST and re.match('/static/', environ['PATH_INFO']):
        return serveFile(environ, start_response)
    
    # リクエスト解析
    request_method, form, valid_csrf = parse_request_application(environ)
    
    # 初期化とフォームの値取得
    msg = "" if valid_csrf else "不正なリクエストです"
    roads_to_display = []
    selected_route = form.get('route_name', [''])[0] if 'route_name' in form else ''
    length_value = form.get('length_value', [''])[0] if 'length_value' in form else ''
    length_op = form.get('length_op', [''])[0] if 'length_op' in form else ''
    sort_column = form.get('sort_column', [''])[0] if 'sort_column' in form else ''
    sort_order = form.get('sort_order', ['ASC'])[0] if 'sort_order' in form else 'ASC'
    edit_mode = False
    edit_kukan_no = None
    url_with_prefecture_application(environ)

    # 編集モード
    if valid_csrf and 'edit' in form:
        edit_kukan_no = form.get('edit_kukan_no', [''])[0]
        if edit_kukan_no:
            edit_mode = True
            msg = f"区間番号 {edit_kukan_no} を編集中です。"

    # キャンセル
    if valid_csrf and 'cancel_update' in form:
        msg = "更新をキャンセルしました。"
        edit_mode = False

    # 各処理の実行
    if valid_csrf and 'bulk_delete' in form:
        msg = process_delete_application(form)

    if valid_csrf and 'add' in form:
        msg = process_add_application(form)
    
    if valid_csrf and 'update' in form:
        msg = process_update_application(form)
        edit_mode = False
    
    if valid_csrf and 'search' in form:
        roads_to_display, msg, selected_route, length_value, length_op, sort_column, sort_order = process_search_application(form)

    # フォームオプション構築
    options = build_form_options_application(selected_route, length_op, sort_column, sort_order)
    
    # 新しいCSRFトークン発行
    csrf_token_local = generate_csrf_token()
    
    # HTML構築
    html_content = build_html_application(msg, roads_to_display, csrf_token_local, options, length_value, length_op, edit_mode, edit_kukan_no)
    html_bytes = html_content.encode('utf-8')
    
    # レスポンス送信
    start_response('200 OK', [
        ('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(html_bytes))),
        ('X-Frame-Options', 'DENY')
    ])
    return [html_bytes]

from wsgiref import simple_server
if __name__ == '__main__':
    LOCALHOST=True
    port = 8080
    # ポート番号
    if len(sys.argv) == 3:
        port = int(sys.argv[2])
    # 都道府県名
    if len(sys.argv) >= 2:
        # URL引数で指定された都道府県名を設定
        if str(sys.argv[1]) in supported_prefectures:
            PREFECTURE.edit_name(str(sys.argv[1]))
        else:
            # 対応していない都道府県名の場合は終了
            print(f"Usage: python3 main.wsgi [{ '|'.join(supported_prefectures) }] [port]", file=sys.stderr)
            sys.exit(1)
    else:
        # 引数がたりない場合は終了
        print(f"Usage: python3 main.wsgi [{ '|'.join(supported_prefectures) }] [port]", file=sys.stderr)
        sys.exit(1)
    createTable()
    importCSV()
    server = simple_server.make_server('', port, application)
    sys.stderr.write(f"サーバーを起動しました: http://localhost:{port}\n")
    server.serve_forever()