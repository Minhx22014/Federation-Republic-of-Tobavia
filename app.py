import os
import json
from flask import Flask, request, redirect, session, render_template

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

# Danh sách file cho phép chỉnh sửa
ALLOWED_FILES = [
    "index.html", "Bieutrung.html", "Cacbang.html",
    "Caccoquanchinhphu.html", "Cacquanchucchinhphu.html",
    "Hienphapluat.html", "news.html"
]

USERNAME = "admin"
PASSWORD = "123456"
NEWS_FILE = "news.json"

# Lấy đường dẫn thư mục gốc của dự án
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_news():
    filepath = os.path.join(BASE_DIR, NEWS_FILE)
    if not os.path.exists(filepath): return []
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else []

def save_news(news_list):
    filepath = os.path.join(BASE_DIR, NEWS_FILE)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)

def is_logged_in():
    return session.get("logged_in")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["logged_in"] = True
            return redirect("/admin")
        return "Sai tài khoản"
    return '<form method="post"><input name="username" placeholder="User"><br><input name="password" type="password" placeholder="Pass"><br><button type="submit">Login</button></form>'

@app.route("/page/<filename>")
def show_page(filename):
    if filename not in ALLOWED_FILES: return "Không tồn tại"
    return render_template(filename)

@app.route("/admin/edit/<filename>", methods=["GET", "POST"])
def edit(filename):
    if not is_logged_in():
        return redirect("/login")
    if filename not in ALLOWED_FILES:
        return "File không hợp lệ"

    filepath = os.path.join(BASE_DIR, "templates", filename)

    if request.method == "POST":
        # Lấy nội dung từ form
        content = request.form["content"]

        # Chuẩn hóa newline từ textarea
        content = content.replace('\r\n', '\n').replace('\r', '\n')

        # Ghi vào file, để Python tự chuyển \n → \r\n trên Windows
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return redirect(f"/page/{filename}")

    # Đọc file để hiển thị trong textarea
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return f"Lỗi: Không thấy file tại {filepath}"

    return f'''
    <h2>Đang chỉnh: {filename}</h2>
    <form method="post">
        <textarea name="content" rows="25" cols="100">{content}</textarea><br>
        <button type="submit">Lưu</button>
    </form>
    '''
@app.route("/admin")
def admin_panel():
    if not is_logged_in(): return redirect("/login")
    links = "".join([f"<li>{f} | <a href='/page/{f}'>Xem</a> | <a href='/admin/edit/{f}'>Sửa</a></li>" for f in ALLOWED_FILES])
    return f"<h1>Admin Panel</h1><ul>{links}</ul><a href='/admin/news'>Đăng tin tức</a><br><a href='/logout'>Logout</a>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/admin/news", methods=["GET", "POST"])
def admin_news():
    if not is_logged_in(): return redirect("/login")
    if request.method == "POST":
        news_list = load_news()
        news_list.append({"title": request.form["title"], "content": request.form["content"]})
        if len(news_list) > 5: news_list.pop(0)
        save_news(news_list)
        return redirect("/news")
    return '<h2>Đăng tin</h2><form method="post"><input name="title" placeholder="Tiêu đề"><br><textarea name="content" rows="10" cols="80"></textarea><br><button type="submit">Đăng</button></form>'

@app.route("/news")
def show_news():
    return render_template("news.html", news_list=load_news())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)