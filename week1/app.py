from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = "guestbook.db"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            CREATE TABLE messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                message TEXT
            )
        """)
        conn.commit()
        conn.close()

def get_conn():
    return sqlite3.connect(DB_PATH)

@app.route('/')
def home():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, name, message FROM messages ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return render_template('index.html', messages=rows)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    return f"검색어: {query}"

@app.route('/write', methods=['POST'])
def write():
    name = request.form.get('name', '')
    message = request.form.get('message', '')
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO messages (name, message) VALUES (?, ?)", (name, message))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
