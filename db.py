import os
import psycopg2,hashlib,string,random
import datetime

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)

    return connection

# ランダムなソルトを生成
def get_salt():
  # 文字列の候補(英大小文字 + 数字)
  charset = string.ascii_letters + string.digits

  # charset からランダムに30文字取り出して結合
  salt = ''.join(random.choices(charset, k=30))
  return salt

# ソルトとPWからハッシュ値を生成
def get_hash(password, salt):
  b_pw = bytes(password, "utf-8")
  b_salt = bytes(salt, "utf-8")
  hashed_password = hashlib.pbkdf2_hmac("sha256", b_pw, b_salt, 1000).hex()
  return hashed_password


# ユーザ登録
def insert_user(user_name, mail,password ):
    sql = 'INSERT INTO users VALUES (default, %s, %s, %s, %s)'
    salt = get_salt()  # ソルトの生成
    hashed_password = get_hash(password, salt)  # 生成したソルトでハッシュ

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(sql, (user_name, hashed_password, salt, mail))
        count = cursor.rowcount  # 更新件数を取得
        connection.commit()

    except psycopg2.DatabaseError:
        count = 0

    finally:
        cursor.close()
        connection.close()

    return count

#ログイン
def login(password,mail):
  sql = 'SELECT * FROM users WHERE mail = %s'

  flg = False
  try :
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(sql,(mail,))
    users = cursor.fetchone()
    if users != None:
      salt =  users[3]
      hashed_password = get_hash(password,salt)
      if hashed_password ==users[2]:
        flg = True
  except psycopg2.DatabaseError:
    flg = False
  finally:
    cursor.close()
    connection.close()
  return flg

#利用者詳細
def select_user_detail(user_id):
  connection = get_connection()
  cursor = connection.cursor()
  sql = 'SELECT * FROM users WHERE user_id = %s'

  cursor.execute(sql,(user_id,))
  rows = cursor.fetchall()
  connection.close()
  cursor.close()

  return rows



#本の全件取得
def select_all_books():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM books'

    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.close()
    cursor.close()

    return rows


#本の詳細表示
def select_book_detail(isbn):
  connection = get_connection()
  cursor = connection.cursor()
  sql = 'SELECT * FROM books WHERE isbn = %s'

  cursor.execute(sql,(isbn,))
  rows = cursor.fetchall()
  connection.close()
  cursor.close()
  if rows:
        book = {
            'id': rows[0][0],
            'title': rows[0][1],
            'author': rows[0][2],
            'publisher': rows[0][3],
            'isbn': rows[0][4]
        }
        return book
  else:
        return None



#本の登録
def insert_book(title, author, publisher, isbn):
    sql = 'INSERT INTO books VALUES (default, %s, %s, %s, %s)'
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(sql, (title, author, publisher, isbn))
        count = cursor.rowcount  # 更新件数を取得
        connection.commit()
    except psycopg2.DatabaseError:
        count = 0
    finally:
        cursor.close()
        connection.close()

    return count


def insert_category(category):
  connection = get_connection()
  cursor = connection.cursor()

  sql = 'INSERT INTO book_category VALUES (default , %s)'
  cursor.execute(sql, (category,))
  cursor.close()
  connection.close()

#本のタイトル検索
def select_title_book(title):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM books WHERE title LIKE %s'

    search_pattern = f'%{title}%'

    cursor.execute(sql, (search_pattern,))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


#本の編集
def edit_book(title, id):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'UPDATE books SET title = %s WHERE id = %s'
    cursor.execute(sql, (title, id))
    connection.commit()
    cursor.close()
    connection.close()

#図書の削除
def delete_book(id):
  connection = get_connection()
  cursor = connection.cursor()
  sql = 'DELETE FROM books WHERE id =%s'
  cursor.execute(sql, (id,))
  connection.commit()
  cursor.close()
  connection.close()

  #図書の貸出
def create_lending(book_id, user_id):
    connection = get_connection()
    cursor = connection.cursor()

    lending_date = datetime.datetime.now()  # 現在の日時を取得

    sql = 'INSERT INTO lending (book_id, user_id, lending_date) VALUES (%s, %s, %s)'

    try:
        cursor.execute(sql, (book_id, user_id, lending_date))
        connection.commit()
        lending_id = cursor.lastrowid  # 作成された貸出IDを取得
    except psycopg2.DatabaseError:
        lending_id = None
    finally:
        cursor.close()
        connection.close()

    return lending_id









