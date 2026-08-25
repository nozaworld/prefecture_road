#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import io
import re
import textwrap

# CGIモジュールをインポート
import cgi
import cgitb
cgitb.enable()

localhost=False

# sqlite3（SQLサーバ）モジュールをインポート
import sqlite3

# データベースファイルのパスを設定
app_dir = os.path.dirname(os.path.abspath(__file__))
dbname = os.path.join(app_dir, 'database.db')

# テーブルの作成
def createTable():
    # データベース接続とカーソル生成
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    # テーブルの作成
    create_table = 'create table if not exists users (id int, name varchar(64))'
    cur.execute(create_table)
    # コミット（変更を確定）
    con.commit()
    # カーソルと接続を閉じる
    cur.close()
    con.close()

createTable()

# 学生情報のデータベースへの登録
def registerStudent(std_id, std_name):
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    con.text_factory = str

    # SQL文（insert）の作成と実行
    sql = 'insert into users (id, name) values (?,?)'
    cur.execute(sql, (std_id, std_name))
    con.commit()

    cur.close()
    con.close()

# 登録情報一覧の取得
def getAllstudents():
    # データベース接続とカーソル生成
    con = sqlite3.connect(dbname)
    cur = con.cursor()
    con.text_factory = str

    # SQL文（select）の作成と実行
    sql = 'select * from users'
    cur.execute(sql)
    lists = cur.fetchall()

    cur.close()
    con.close()

    return lists

# CSSファイルなどを送信（リファレンスWEBサーバ実行時のみ使用）
def serveFile(environ,start_response):
    # 拡張子とコンテンツタイプ（必要に応じて追加すること）
    types = {'.css': 'text/css', '.jpg': 'image/jpg', '.png': 'image/png'}
    
    # static ディレクトリ以下の指定ファイルを開いてその内容を返す．
    # ファイルが無ければエラーを返す．
    #
    assert(re.match('/static/', environ['PATH_INFO']))
    filepath = '{dir}/{path}'.format(dir=app_dir, path=environ['PATH_INFO'])
    ext  = os.path.splitext(filepath)[1]
    
    if os.path.isfile(filepath) and ext in types:
        try:
            with open(filepath, "rb") as f:
                r = f.read()
            binary_stream = io.BytesIO(r)
        except:
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [b"Internal server error"]
    else:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b"Not found."]

    start_response('200 OK', [('Content-Type', types[ext])])
    return binary_stream

# アプリケーション本体
def application(environ,start_response):

    if localhost and re.match('/static/', environ['PATH_INFO']):
        ''' リファレンスWEBサーバ実行時のみ
             このwsgiスクリプトを実行しているカレントディレクトリ以下に
             static というディレクトリを作って，default.cssというファイルを置いておくと，
             http://localhost:8080/static/default.css でファイルがダウンロードできる．
        '''
        return serveFile(environ,start_response)

    # HTML（共通テンプレート）
    tmpl = textwrap.dedent('''
    <html lang="ja">
    <head>
    <meta charset="UTF-8">
    <title>WSGI テスト</title>
    <link rel="stylesheet" href="/static/default.css"> 
    </head>
    {body}
    </html>
    ''')

    # フォームデータを取得
    form = cgi.FieldStorage(environ=environ,keep_blank_values=True)

    if 'register' in form:
        # 入力フォームで登録ボタンがクリックされた場合

        # フォームデータから各フィールド値を取得
        v1 = form.getvalue("v1")
        v2 = form.getvalue("v2")

        if v1 != '' and v2 != '':
            # データベースへ学生の登録
            registerStudent(int(v1), v2)
            msg = '登録しました。'
        else:
            msg = '登録失敗：空になっている入力項目があります。'

        # データベースの登録情報一覧の取得
        students_list = getAllstudents()

        # 一覧のHTML形式への変換
        list = ''
        for row in students_list:
            list += f'<li>{str(row[0])}, {row[1]}</li>\n'

        bcontent = textwrap.dedent('''
        <body>
        <p>{message}</p>
        <hr>
        <div class="ol1">
        <h2>一覧表示</h2>
        <ul>
        {slist}
        </ul>
        </div>
        <a href="./sample.wsgi">登録ページに戻る</a>
        </body>
        ''').format(message=msg, slist=list)

    else:
        # デフォルトページ（入力フォーム表示）

        # HTML（入力フォーム部分）
        bcontent = textwrap.dedent('''
        <body>
        <div class=header>入力フォーム</div>
        <div class="form1">
        <form>
        学生番号（整数） <input type="text" name="v1"><br>
        氏名　（文字列） <input type="text" name="v2"><br>
        <button type="submit" name="register">登録</button>
        </form>
        </div>
        </body>
        ''')


    html = tmpl.format(body=bcontent)
    html = html.encode('utf-8')

    # レスポンス
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8'),
        ('Content-Length', str(len(html))) ])
    return [html]


# リファレンスWEBサーバを起動
#  ファイルを直接実行する（python3 sample.wsgi）と，
#  リファレンスWEBサーバが起動し，http://localhost:8080 にアクセスすると
#  このサンプルの動作が確認できる．
#  コマンドライン引数にポート番号を指定（python3 sample.wsgi ポート番号）した場合は，
#  http://localhost:ポート番号 にアクセスする．
from wsgiref import simple_server
if __name__ == '__main__':
    port = 8080
    localhost = True
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    server = simple_server.make_server('', port, application)
    server.serve_forever()
