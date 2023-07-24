from flask import Flask, render_template, request,redirect,url_for,session
import random,string
import db,string,random
from datetime import timedelta



app = Flask(__name__)

app.secret_key=''.join(random.choices(string.ascii_letters, k=256))
#トップページ
@app.route('/', methods=['GET'])
def index():
    msg = request.args.get('msg')   # Redirect された時のパラメータ受け取り

    if msg == None:
        # 通常のアクセスの場合
        return render_template('index.html')
    else :
        # register_exe() から redirect された場合
        return render_template('index.html', msg=msg)
#ユーザ登録遷移
@app.route('/register')
def register():
    return render_template('u_register.html')

# ユーザ登録確認画面
@app.route('/u_register', methods=['POST'])
def u_register():
    user_name = request.form.get('user_name')
    mail = request.form.get('mail')
    password = request.form.get('password')

    # パリデーションチェック
    if user_name == '':
        error = 'ユーザ名が未入力です'
        return render_template('u_register.html', error=error)

    if mail == '':
        error = 'メールアドレスが未入力です'
        return render_template('u_register.html', error=error)

    if password == '':
        error = 'パスワードが未入力です'
        return render_template('u_register.html', error=error)

    session['user_name'] = user_name
    session['mail'] = mail
    session['password'] = password

    return render_template('register_confirm.html', user_name=user_name, mail=mail,password=password,)



# ユーザ登録実行
@app.route('/u_register_exe', methods=['POST'])
def u_register_exe():
    user_name = session.get('user_name')
    mail = session.get('mail')
    password = session.get('password')

    count = db.insert_user(user_name,  mail, password)

    if count == 1:
        msg = '登録が完了しました。'
        return render_template('success.html', msg=msg)
    else:
        error = '登録に失敗しました。'
        return render_template('u_register.html', error=error)



#ログイン遷移
@app.route('/',methods=['POST'])
def login():
    password = request.form.get('password')
    mail = request.form.get('mail')

    if db.login(password,mail):
        session['users'] = True
        session['users_detail'] = {'password':password,'mail':mail}
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=60)
        return redirect(url_for('b_list'))
    else :
        error = 'メールアドレスまたはパスワードが違います'


        input_data = {'password':password,'mail':mail}
        return render_template('index.html' , error= error,data =input_data)

#マイページ
@app.route('/mypage',methods = ['get'])
def mypage():
    if 'users' in session:
        book_list = db.select_all_books()
        return render_template('list.html',books=book_list)
    else:
        return redirect(redirect('index'))





#図書登録遷移
@app.route('/book_register')
def book_register():
    return render_template('book_register.html')

#図書登録確認画面
@app.route('/book_register_confirm', methods=['POST'])
def book_register_confirm():
    title = request.form.get('title')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    isbn = request.form.get('isbn')

    if title == '':
        error = 'タイトルが未入力です'
        return render_template('book_register.html', error=error)

    if author == '':
        error = '著者が未入力です'
        return render_template('book_register.html', error=error)

    if publisher == '':
        error = '出版社が未入力です'
        return render_template('book_register.html', error=error)

    if isbn == '':
        error = 'ISBNが未入力です'
        return render_template('book_register.html', error=error)

    session['title'] = title
    session['author'] = author
    session['publisher'] = publisher
    session['isbn'] = isbn

    return render_template('book_register_confirm.html', title=title, author=author, publisher=publisher, isbn=isbn)

#図書登録（データベース）
@app.route('/book_register_exe', methods=['POST'])
def book_register_exe():
    title = session.get('title')
    author = session.get('author')
    publisher = session.get('publisher')
    isbn = session.get('isbn')

    db.insert_book(title, author, publisher, isbn)
    book_list = db.select_all_books()
    return render_template('list.html', books=book_list)

#図書の一覧表示
@app.route('/b_list', methods = ['get'])
def b_list():
    book_list = db.select_all_books()
    return render_template('list.html', books = book_list)


#図書のタイトル検索
@app.route('/select_title_book', methods=['GET'])
def select_title_book():
    title = request.args.get('title')
    book_list = db.select_title_book(title)
    return render_template('list.html', books=book_list)

#図書の詳細表示
@app.route('/detail', methods=['GET'])
def book_detail():
    book_id = request.args.get('book_id')
    title = request.args.get('title')
    author = request.args.get('author')
    publisher = request.args.get('publisher')
    isbn = request.args.get('isbn')

    book = db.select_book_detail(isbn)

    session['book_id'] = book_id

    return render_template('book_detail.html', book=book)



@app.route('/edit', methods=['GET'])
def book_edit():
    book_id = request.args.get('book_id')
    title = request.args.get('title')
    return render_template('book_edit.html', id=book_id,title=title)


#図書の編集
@app.route('/book_edit_exe' , methods  =['post'])
def book_edit_exe():
    id = request.form.get('id')
    title = request.form.get('title')
    db.edit_book(title,id)
    book_list = db.select_all_books()
    return render_template('list.html', books = book_list)

@app.route('/book_delete', methods=['GET'])
def book_delete():
    book_id = request.args.get('book_id')
    return render_template('book_delete.html', id=book_id)

@app.route('/book_delete_exe' , methods  =['post'])
def book_delete_exe():
    id = request.form.get('id')
    db.delete_book(id)
    book_list = db.select_all_books()
    return render_template('list.html', books = book_list)

#ログアウト
@app.route('/logout')
def logout():
    session.pop('user', None) # session の破棄
    return  redirect(url_for('index')) # ログイン画面にリダイレクト

if __name__ == "__main__":
    app.run(debug=True)
