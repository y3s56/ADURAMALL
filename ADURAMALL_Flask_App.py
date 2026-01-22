# ADURAMALL - Full Startup-Ready Prototype (Python/Flask)
# Features:
# - Green ocean-themed background
# - Designer collections (clothes, pants, footwear)
# - Promo tags on products
# - User registration/login
# - Real human avatar upload per customer
# - AI try-on placeholder
# - Cart & checkout mock
# - Mobile-friendly UI

from flask import Flask, render_template_string, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = 'aduramall-secret'

# ----------------- Safe Folder Setup for Windows -----------------
UPLOAD_FOLDER = 'static/avatars'
if os.path.exists(UPLOAD_FOLDER):
    if not os.path.isdir(UPLOAD_FOLDER):
        os.remove(UPLOAD_FOLDER)  # delete file if a file exists with the same name
        os.makedirs(UPLOAD_FOLDER)
else:
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ----------------- Sample Products -----------------
products = [
    {"id": 1, "name": "Ocean Breeze Dress", "category": "Clothes", "price": 120, "promo": "20% OFF", "image": "https://images.unsplash.com/photo-1520975916090-3105956dac38"},
    {"id": 2, "name": "Green Wave Pants", "category": "Pants", "price": 90, "promo": "Buy 1 Get 1 50%", "image": "https://images.unsplash.com/photo-1542060748-10c28b62716f"},
    {"id": 3, "name": "Seafoam Sneakers", "category": "Footwear", "price": 150, "promo": "Free Shipping", "image": "https://images.unsplash.com/photo-1528701800489-20be3c48d5e4"}
]

# ----------------- Users -----------------
users = {"admin": "admin"}

# ----------------- HTML Template -----------------
html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ADURAMALL</title>
<style>
body{margin:0;font-family:Arial;background:linear-gradient(rgba(0,80,40,.85),rgba(0,80,40,.85)),url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e');background-size:cover;color:#f0fff4}
header{padding:25px;text-align:center;font-size:48px;font-weight:bold;letter-spacing:4px}
nav{text-align:center;margin-bottom:10px}
nav a{color:#86efac;margin:0 12px;text-decoration:none;font-weight:bold}
section{padding:20px}
.products{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:20px}
.card{background:rgba(0,0,0,.55);border-radius:18px;padding:15px;box-shadow:0 0 20px rgba(0,0,0,.4)}
.card img{width:100%;border-radius:12px;height:260px;object-fit:cover}
.promo{background:#22c55e;color:#022c22;padding:6px 10px;border-radius:10px;display:inline-block;margin-top:8px;font-weight:bold}
.tryon{display:flex;gap:20px;flex-wrap:wrap}
.avatar-box{position:relative;width:300px}
.avatar-box img{width:100%;border-radius:16px}
.cloth-overlay{position:absolute;top:80px;left:60px;width:180px;display:none}
button{background:#16a34a;color:#022c22;border:none;padding:10px 14px;border-radius:10px;cursor:pointer;margin:3px}
input{padding:8px;border-radius:8px;border:none;margin:5px}
footer{text-align:center;padding:20px;opacity:.8}
</style>
</head>
<body>
<header>ADURAMALL</header>
<nav>
<a href="/">Home</a>
<a href="/cart">Cart ({{cart_count}})</a>
{% if user %}<b>Welcome {{user}}</b> | <a href='/logout'>Logout</a>{% else %}<a href='/login'>Login</a>{% endif %}
</nav>

<section>
<h2>Designer Collections</h2>
<div class="products">
{% for p in products %}
<div class="card">
<img src="{{p.image}}">
<h3>{{p.name}}</h3>
<p>{{p.category}}</p>
<p><b>$ {{p.price}}</b></p>
<div class="promo">{{p.promo}}</div><br>
<a href="/add/{{p.id}}"><button>Add to Cart</button></a>
<button onclick="tryOn('{{p.image}}')">Try on Avatar</button>
</div>
{% endfor %}
</div>
</section>

<section>
<h2>Upload Your Human Avatar</h2>
{% if avatar %}<img src='{{avatar}}' width='260' style='border-radius:20px'><br>{% endif %}
<form action='/upload_avatar' method='post' enctype='multipart/form-data'>
<input type='file' name='avatar' accept='image/*' required>
<button>Upload My Face</button>
</form>
</section>

<section>
<h2>Virtual Try-On (Demo)</h2>
<div class="tryon">
<div class="avatar-box">
<img src="https://images.unsplash.com/photo-1607746882042-944635dfe10e">
<img id="cloth" class="cloth-overlay">
</div>
<p>Select a product and click Try On to preview it on your avatar.</p>
</div>
</section>

<footer>© 2026 ADURAMALL — Fashion inspired by the ocean</footer>
<script>
function tryOn(src){let c=document.getElementById('cloth');c.src=src;c.style.display='block';}
</script>
</body>
</html>
"""

# ----------------- Routes -----------------
@app.route('/')
def home():
    cart = session.get('cart', [])
    avatar = session.get('avatar', None)
    return render_template_string(html, products=products, cart_count=len(cart), user=session.get('user'), avatar=avatar)

@app.route('/add/<int:pid>')
def add(pid):
    cart = session.get('cart', [])
    cart.append(pid)
    session['cart'] = cart
    return redirect('/')

@app.route('/cart')
def cart():
    cart_ids = session.get('cart', [])
    items = [p for p in products if p['id'] in cart_ids]
    total = sum(i['price'] for i in items)
    return render_template_string("""
<h1>ADURAMALL Cart</h1>
{% for i in items %}<p>{{i.name}} - ${{i.price}}</p>{% endfor %}
<h3>Total: ${{total}}</h3>
<a href='/'>Back</a>
""", items=items, total=total)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        if users.get(request.form['u'])==request.form['p']:
            session['user'] = request.form['u']
            return redirect('/')
    return render_template_string("""
<h2>Login - ADURAMALL</h2>
<form method='post'>
<input name='u' placeholder='username'>
<input name='p' placeholder='password' type='password'>
<button>Login</button></form>
<a href='/'>Home</a>
""")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'avatar' in request.files:
        file = request.files['avatar']
        filename = f'user_{session.get("user","guest")}.png'
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        # Use URL path for HTML
        session['avatar'] = f'/static/avatars/{filename}'
    return redirect('/')

# ----------------- Run Flask App -----------------
if __name__ == '__main__':
    print("Starting ADURAMALL Flask server on http://127.0.0.1:5000")
    app.run(debug=True)
