from flask import Flask, render_template, request, redirect, session, flash
import os

app = Flask(__name__)
app.secret_key = 'secret123'

# Upload folder
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Dummy posts
posts = []

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('home.html', posts=posts)

# ---------------- CREATE POST ----------------
@app.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image = request.files.get('image')

        filename = ""
        if image and image.filename != "":
            filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        post = {
            'id': len(posts) + 1,
            'title': title,
            'content': content,
            'image': filename,
            'author': 'Admin'
        }

        posts.append(post)
        return redirect('/')

    return render_template('create_post.html')

# ---------------- BLOG DETAIL ----------------
@app.route('/post/<int:id>')
def post_detail(id):
    post = posts[id - 1]
    return render_template('blog_detail.html', post=post)

# ================= ADMIN =================

# 🔐 Admin Login
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/dashboard')
        else:
            flash("Invalid Username or Password")

    return render_template('admin_login.html')

# 📊 Dashboard
@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/admin')

    return render_template('dashboard.html', posts=posts)

# ❌ Delete Post
@app.route('/delete/<int:id>')
def delete_post(id):
    if not session.get('admin'):
        return redirect('/admin')

    if id <= len(posts):
        posts.pop(id - 1)

    return redirect('/dashboard')

# 🚪 Logout
@app.route('/admin-logout')
def admin_logout():
    session.clear()
    return redirect('/admin')

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)