from flask import Flask, render_template_string, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'aduramall-secret'

# --------- Sample products ---------
products = [
    {"id": 1, "name": "Ocean Breeze Dress", "category": "Clothes", "price": 120, "promo": "20% OFF", "image": "https://images.unsplash.com/photo-1520975916090-3105956dac38"},
    {"id": 2, "name": "Green Wave Pants", "category": "Pants", "price": 90, "promo": "Buy 1 Get 1 50%", "image": "https://images.unsplash.com/photo-1542060748-10c28b62716f"},
    {"id": 3, "name": "Seafoam Sneakers", "category": "Footwear", "price": 150, "promo": "Free Shipping", "image": "https://images.unsplash.com/photo-1528701800489-20be3c48d5e4"},
    {"id": 4, "name": "Coral Top", "category": "Clothes", "price": 80, "promo": "15% OFF", "image": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f"}
]

# --------- Users ---------
users = {"admin": "admin"}

# --------- Templates ---------
base_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{{ title }}</title>
<style>
body {
    margin:0; font-family:Arial;
    background: linear-gradient(rgba(0,80,40,0.85), rgba(0,80,40,0.85)),
                url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e');
    background-size:cover; color:#f0fff4; text-align:center;
}
header { padding:25px; font-size:48px; font-weight:bold; letter-spacing:4px; text-shadow:2px 2px 8px #022c22; }
nav a { color:#86efac; margin:0 12px; text-decoration:none; font-weight:bold;}
section { padding:20px; }
button { background:#16a34a; color:#022c22; border:none; padding:10px 14px; border-radius:10px; cursor:pointer; margin:3px; transition:0.2s;}
button:hover { transform: scale(1.05); }
input { padding:8px; border-radius:8px; border:none; margin:5px; }

.grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:20px; }
.card { background: rgba(0,0,0,.55); border-radius:18px; padding:15px; transition: transform 0.2s; }
.card:hover { transform: scale(1.05); }
.card img { width:100%; height:260px; object-fit:cover; border-radius:12px; }
.promo { background:#22c55e; color:#022c22; padding:6px; border-radius:10px; margin-top:5px; font-weight:bold; }

.filters button { background:#22c55e; color:#022c22; border:none; padding:8px 12px; border-radius:10px; margin:5px; font-weight:bold; transition:0.2s;}
.filters button:hover { transform: scale(1.1); background:#16a34a; }

.carousel-container { position:relative; overflow:hidden; margin:20px auto; max-width:1000px; }
.carousel-track { display:flex; transition: transform 0.5s ease; gap:20px; }
.carousel-btn { position:absolute; top:50%; transform:translateY(-50%); background: rgba(34,197,94,0.8); color:#022c22; border:none; padding:10px 15px; font-size:24px; border-radius:50%; cursor:pointer; z-index:10; }
.carousel-btn.left { left:10px; } 
.carousel-btn.right { right:10px; }
.carousel-btn:hover { background:#16a34a; }

.tryon { display:flex; justify-content:center; gap:20px; flex-wrap:wrap; margin-top:20px; }
.avatar-box { position:relative; width:300px; }
.avatar-box img { width:100%; border-radius:16px; }
.cloth-overlay { position:absolute; top:80px; left:60px; width:180px; display:none; }

footer { text-align:center; padding:20px; opacity:.8; margin-top:40px; }

@media(max-width:600px){
  .grid { grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); }
  header { font-size:36px; }
  .carousel-btn { font-size:20px; padding:8px 12px; }
}
</style>
</head>
<body>

<header>ADURAMALL</header>
<nav>
<a href="{{ url_for('home') }}">Home</a>
<a href="{{ url_for('cart') }}">Cart ({{ cart_count }})</a>
{% if user %}<b>Welcome {{ user }}</b> | <a href="{{ url_for('logout') }}">Logout</a>{% else %}<a href="{{ url_for('login') }}">Login</a> | <a href="{{ url_for('register') }}">Register</a>{% endif %}
</nav>

{% block content %}{% endblock %}

<footer>© 2026 ADURAMALL — Fashion inspired by the ocean</footer>

<script>
function filterCategory(cat){
  let cards = document.querySelectorAll('.product-card');
  cards.forEach(c => { c.style.display = (cat=='All'||c.dataset.category==cat) ? 'block':'none'; });
}
let carouselIndex=0;
function moveCarousel(direction){
    const track=document.getElementById('featured-carousel');
    const cardWidth=track.querySelector('.card').offsetWidth + 20;
    const visibleCards=Math.floor(track.parentElement.offsetWidth / cardWidth);
    const maxIndex=track.children.length-visibleCards;
    carouselIndex+=direction;
    if(carouselIndex<0) carouselIndex=0;
    if(carouselIndex>maxIndex) carouselIndex=maxIndex;
    track.style.transform=`translateX(${-carouselIndex*cardWidth}px)`;
}
function tryOn(src){
    let c=document.getElementById('cloth'); c.src=src; c.style.display='block';
}
</script>

</body>
</html>
"""

# --------- Routes ---------
@app.route('/')
def home():
    cart=session.get('cart',[])
    avatar=session.get('avatar',None)
    return render_template_string("""
{% extends base_html %}
{% block content %}
<section class="filters">
<h2>Browse by Category</h2>
<button onclick="filterCategory('All')">All</button>
<button onclick="filterCategory('Clothes')">Clothes</button>
<button onclick="filterCategory('Pants')">Pants</button>
<button onclick="filterCategory('Footwear')">Footwear</button>
</section>

<section>
<h2>🌟 Featured Items</h2>
<div class="carousel-container">
<div class="carousel-track" id="featured-carousel">
{% for p in products[:4] %}
<div class="card product-card" data-category="{{p.category}}">
<img src="{{p.image}}">
<h3>{{p.name}}</h3>
<p><b>$ {{p.price}}</b></p>
<div class="promo">{{p.promo}}</div>
<button onclick="tryOn('{{p.image}}')">Try On</button>
<a href="{{ url_for('add_to_cart', pid=p.id) }}"><button>Add to Cart</button></a>
</div>
{% endfor %}
</div>
<button class="carousel-btn left" onclick="moveCarousel(-1)">&#10094;</button>
<button class="carousel-btn right" onclick="moveCarousel(1)">&#10095;</button>
</div>
</section>

<section>
<h2>🆕 New Arrivals</h2>
<div class="grid">
{% for p in products[1:] %}
<div class="card product-card" data-category="{{p.category}}">
<img src="{{p.image}}">
<h3>{{p.name}}</h3>
<p><b>$ {{p.price}}</b></p>
<div class="promo">{{p.promo}}</div>
<button onclick="tryOn('{{p.image}}')">Try On</button>
<a href="{{ url_for('add_to_cart', pid=p.id) }}"><button>Add to Cart</button></a>
</div>
{% endfor %}
</div>
</section>

<section>
<h2>Virtual Try-On Studio</h2>
<div class="tryon">
<div class="avatar-box">
{% if avatar %}
<img src="{{avatar}}">
{% else %}
<img src="https://images.unsplash.com/photo-1607746882042-944635dfe10e" width="260">
{% endif %}
<img id="cloth" class="cloth-overlay">
</div>
<p>Select a product and click “Try On” to preview it on your avatar.</p>
<form action="{{ url_for('upload_avatar') }}" method="post" enctype="multipart/form-data">
<input type="file" name="avatar" accept="image/*" required>
<button>Upload My Face</button>
</form>
</div>
</section>
{% endblock %}
""", base_html=base_html, products=products, cart_count=len(cart), user=session.get('user'), avatar=avatar)

@app.route('/add/<int:pid>')
def add_to_cart(pid):
    cart=session.get('cart',[])
    cart.append(pid)
    session['cart']=cart
    return redirect('/')

@app.route('/cart')
def cart():
    cart_ids=session.get('cart',[])
    items=[p for p in products if p['id'] in cart_ids]
    total=sum(i['price'] for i in items)
    return render_template_string("""
{% extends base_html %}
{% block content %}
<h2>Cart</h2>
{% if items %}
<ul>
{% for i in items %}<li>{{i.name}} - ${{i.price}}</li>{% endfor %}
</ul>
<p><b>Total: ${{total}}</b></p>
<a href="{{ url_for('checkout') }}"><button>Checkout</button></a>
{% else %}
<p>Your cart is empty.</p>
{% endif %}
{% endblock %}
""", base_html=base_html, items=items, total=total, cart_count=len(cart_ids), user=session.get('user'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        if users.get(request.form['u'])==request.form['p']:
            session['user']=request.form['u']
            return redirect('/')
    return render_template_string("""
{% extends base_html %}
{% block content %}
<h2>Login</h2>
<form method="post">
<input name="u" placeholder="Username">
<input name="p" type="password" placeholder="Password">
<button>Login</button>
</form>
{% endblock %}
""", base_html=base_html, cart_count=len(session.get('cart',[])), user=session.get('user'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        users[request.form['u']]=request.form['p']
        session['user']=request.form['u']
        return redirect('/')
    return render_template_string("""
{% extends base_html %}
{% block content %}
<h2>Register</h2>
<form method="post">
<input name="u" placeholder="Username">
<input name="p" type="password" placeholder="Password">
<button>Register</button>
</form>
{% endblock %}
""", base_html=base_html, cart_count=len(session.get('cart',[])), user=session.get('user'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/checkout')
def checkout():
    session['cart']=[]
    return "<h2>Thank you for your purchase!</h2><a href='/'>Home</a>"

@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    if 'avatar' in request.files:
        file=request.files['avatar']
        filename=f'user_{session.get("user","guest")}.png'
        path=f'static/{filename}'
        file.save(path)
        session['avatar']=path
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)
