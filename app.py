from flask import Flask, render_template, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = 'aduramall-secret'

# Avatar upload folder
UPLOAD_FOLDER = 'static/avatars'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Sample products
products = [
    {"id": 1, "name": "Ocean Breeze Dress", "category": "Clothes", "price": 120, "promo": "20% OFF", "image": "https://images.unsplash.com/photo-1520975916090-3105956dac38"},
    {"id": 2, "name": "Green Wave Pants", "category": "Pants", "price": 90, "promo": "Buy 1 Get 1 50%", "image": "https://images.unsplash.com/photo-1542060748-10c28b62716f"},
    {"id": 3, "name": "Seafoam Sneakers", "category": "Footwear", "price": 150, "promo": "Free Shipping", "image": "https://images.unsplash.com/photo-1528701800489-20be3c48d5e4"},
    {"id": 4, "name": "Coral Top", "category": "Clothes", "price": 80, "promo": "15% OFF", "image": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f"}
]

# Users dictionary
users = {"admin": "admin"}

# -------- Routes ---------
@app.route('/')
def home():
    cart = session.get('cart', [])
    avatar = session.get('avatar', None)
    return render_template('home.html', products=products, cart_count=len(cart), user=session.get('user'), avatar=avatar)

@app.route('/add/<int:pid>')
def add_to_cart(pid):
    cart = session.get('cart', [])
    cart.append(pid)
    session['cart'] = cart
    return redirect('/')

@app.route('/cart')
def cart():
    cart_ids = session.get('cart', [])
    items = [p for p in products if p['id'] in cart_ids]
    total = sum(i['price'] for i in items)
    return render_template('cart.html', items=items, total=total, cart_count=len(cart_ids), user=session.get('user'))

@app.route('/checkout')
def checkout():
    session['cart'] = []
    return render_template('checkout.html', cart_count=0, user=session.get('user'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if users.get(username) == password:
            session['user'] = username
            return redirect('/')
    return render_template('login.html', cart_count=len(session.get('cart', [])), user=session.get('user'))

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        users[username] = password
        session['user'] = username
        return redirect('/')
    return render_template('register.html', cart_count=len(session.get('cart', [])), user=session.get('user'))

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
        session['avatar'] = path
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
