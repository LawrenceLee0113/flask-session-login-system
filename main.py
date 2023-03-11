from flask import Flask, session, redirect, url_for, render_template, request, jsonify
from flask_session import Session

import os



accDict = {
    "username": "password",
    "admin123": "123",
    "admin456": "456",
}

users = {
    'username': {'name': 'Alice', 'age': 25},
    'admin123': {'name': 'Bob', 'age': 30},
    'admin456': {'name': 'Charlie', 'age': 35}
}

def checkAccDict(acc,psw):
    try:
        return accDict[acc] == psw
    except KeyError:
        return None
    except Exception:
        return None

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 設定 Session 的密鑰

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/')
def index():
    
    if 'username' in session:
        # 如果已經登入，顯示登入後的頁面
        return render_template('logged_in.html', username=session['username'],nowsession = session)
    else:
        # 如果沒有登入，顯示訪客頁面
        return render_template('guest.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # 在此處檢查用戶名和密碼是否正確，如果正確，則將用戶名儲存在 Session 中
        if checkAccDict(username,password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')

    # 如果是 GET 請求，顯示登入頁面
    return render_template('login.html')


# http://172.20.10.3:1384/logout
@app.route('/logout')
def logout():
    # 在此處清除 Session
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/api/verify', methods=['POST'])
def verify():
    # 从请求的 cookie 中获取 session ID
    if request.method == 'POST':
        session_id = request.form.get('session_id')
        if session_id == session.get('session_id'):
            # session ID 驗證成功，回傳個人資訊
            return jsonify(users[session['username']])
        else:
            # session ID 驗證失敗，回傳錯誤訊息
            return jsonify({'error': 'Invalid session ID'})




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1384, debug=True)