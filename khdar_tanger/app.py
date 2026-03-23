import json
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'khedar_tanger_secret'

def load_db():
    with open('database.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_db(data):
    with open('database.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    db = load_db()
    active_cat = request.args.get('cat', 'الخضروات')
    is_admin = 'user' in session
    return render_template('index.html', db=db, active_cat=active_cat, is_admin=is_admin)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == 'gaffa123': # كلمة مرورك
            session['user'] = 'admin'
            return redirect(url_for('index'))
    return '''<form method="post" style="text-align:center; padding:50px;">
              <input type="password" name="password" placeholder="كلمة المرور">
              <button type="submit">دخول</button></form>'''

@app.route('/update_price', methods=['POST'])
def update_price():
    if 'user' not in session: return "غير مسموح"
    db = load_db()
    item_id, new_p = int(request.form.get('id')), float(request.form.get('price'))
    for cat in db['categories'].values():
        for item in cat:
            if item['id'] == item_id: item['price'] = new_p
    save_db(db); return redirect(request.referrer)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

