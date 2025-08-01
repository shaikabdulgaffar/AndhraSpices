from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import db, User, Restaurant, MenuItem
from flask_sqlalchemy import SQLAlchemy
import os
import random
from datetime import datetime

app = Flask(
    __name__,
    template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')),
    static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)

@app.route('/')
def index():
    restaurants = Restaurant.query.all()
    return render_template('index.html', restaurants=restaurants)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/restaurant/<int:restaurant_id>')
def restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    menu = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
    return render_template('restaurant.html', restaurant=restaurant, menu=menu)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item_id = request.form.get('item_id')
    if not item_id:
        return jsonify({'success': False}), 400
    cart = session.get('cart', {})
    cart[item_id] = cart.get(item_id, 0) + 1
    session['cart'] = cart
    return jsonify({'success': True, 'cart_count': sum(cart.values())})

@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    cart_items = []
    total = 0
    for item_id, qty in cart.items():
        item = MenuItem.query.get(int(item_id))
        if item:
            cart_items.append({'item': item, 'qty': qty})
            total += item.price * qty
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form['fullname']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        username = email  # Use email as username for uniqueness
        if User.query.filter_by(username=username).first():
            return render_template('signup.html', error="Email already exists")
        user = User(
            username=username,
            password=password,
            fullname=fullname,
            mobile=mobile,
            email=email,
            address=address
        )
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/update_cart', methods=['POST'])
def update_cart():
    item_id = request.form.get('item_id')
    delta = request.form.get('delta', 0)
    cart = session.get('cart', {})
    if delta == "delete":
        if item_id in cart:
            del cart[item_id]
    else:
        delta = int(delta)
        if item_id in cart:
            if delta == -1 and cart[item_id] > 1:
                cart[item_id] -= 1
            elif delta == 1:
                cart[item_id] += 1
            # Agar qty 1 hai aur -1 click hua toh kuch na karo
        elif delta > 0:
            cart[item_id] = 1
    session['cart'] = cart
    qty = cart.get(item_id, 0)
    return jsonify({'success': True, 'qty': qty, 'cart_count': sum(cart.values())})

@app.route('/clear_cart', methods=['POST'])
def clear_cart():
    session['cart'] = {}
    return jsonify({'success': True})

@app.context_processor
def inject_user():
    user = None
    if session.get('user_id'):
        user = User.query.get(session['user_id'])
    return dict(user=user)

@app.context_processor
def inject_now():
    return {'now': datetime.now}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Restaurant.query.count() == 0:
            # Restaurant data
            restaurant_data = [
    ("The Spice Room", "Finest Indian Recipes", 4.5, "/static/images/restaurant1.png"),
    ("Flavour Junction", "Chef’s Special Menu", 4.2, "/static/images/restaurant2.png"),
    ("Royal Feast", "Delicious Food, Crafted Fresh", 4.3, "/static/images/restaurant3.png"),
    ("Gourmet Lane", "Handpicked Culinary Delights", 4.1, "/static/images/restaurant4.png"),
    ("Tadka House", "Taste That Inspires", 4.4, "/static/images/restaurant5.png"),
    ("Zaika Palace", "Authentic Flavours, Modern Touch", 4.6, "/static/images/restaurant6.png"),
    ("Bistro Bites", "Quality Ingredients, Great Taste", 4.2, "/static/images/restaurant7.png"),
    ("Delight Kitchen", "A Feast for Every Mood", 4.3, "/static/images/restaurant8.png"),
    ("Flavoursome Kitchen", "Satisfying Every Craving", 4.5, "/static/images/restaurant9.png"),
    ("Gourmet Thali", "Made with Passion", 4.1, "/static/images/restaurant10.png"),
    ("Magic Platter", "Simply Good Food", 4.2, "/static/images/restaurant11.png"),
    ("Kurry House", "Freshly Prepared Dishes", 4.3, "/static/images/restaurant12.png"),
    ("Heritage House", "Unique Taste Experience", 4.6, "/static/images/restaurant13.png"),
    ("Royal Lane", "Flavours You’ll Love", 4.4, "/static/images/restaurant14.png"),
    ("Chettinad Corner", "Food That Makes You Smile", 4.5, "/static/images/restaurant15.png"),
    ("Darbar Dine", "A Journey of Taste", 4.2, "/static/images/restaurant16.png"),
    ("Chefs Table", "Enjoy Every Bite", 4.3, "/static/images/restaurant17.png"),
    ("Valley Kitchen", "Memorable Meals", 4.4, "/static/images/restaurant18.png"),
    ("Aroma House", "Classic Meets Contemporary", 4.1, "/static/images/restaurant19.png"),
    ("Delicacies Hub", "Your Favourite Food Destination", 4.2, "/static/images/restaurant20.png"),
]
            # Food items mapping by restaurant name
            food_items_by_restaurant = {
    "The Spice Room": [
        ("Red Velvet Cake", 120, 4.7, "/static/images/Red Velvet Cake.png"),
        ("Chocolate Cake", 110, 4.6, "/static/images/Chocolate Cake.png"),
        ("Cupcakes", 80, 4.5, "/static/images/Cupcakes.png"),
        ("Papdi Chaat", 60, 4.4, "/static/images/Papdi Chaat.png"),
        ("Avocado and Egg Plate", 150, 4.8, "/static/images/Avocado and Egg Plate.png"),
        ("Classic American Breakfast", 140, 4.7, "/static/images/Classic American Breakfast.png"),
        ("Paniyaram", 70, 4.5, "/static/images/Paniyaram.png"),
        ("Pasta Salad", 100, 4.6, "/static/images/Pasta Salad.png"),
        ("Meleate Dosa", 90, 4.4, "/static/images/Meleate Dosa.png"),
        ("Masala Vada", 60, 4.3, "/static/images/Masala Vada.png"),
        ("Dosa", 80, 4.5, "/static/images/Dosa.png"),
        ("Chicken Biryani", 180, 4.8, "/static/images/Chicken Biryani.png"),
        ("Special Chicken Biryani", 200, 4.9, "/static/images/Special Chicken Biryani.png"),
    ],
    "Flavour Junction": [
        ("Laccha Paratha", 50, 4.2, "/static/images/Laccha Paratha.png"),
        ("Special Samosa", 40, 4.1, "/static/images/Special Samosa.png"),
        ("Special Idli", 60, 4.3, "/static/images/Special Idli.png"),
        ("Fruit Curd Rice", 90, 4.5, "/static/images/Fruit Curd Rice.png"),
        ("Mutton Biryani", 220, 4.9, "/static/images/Mutton Biryani.png"),
        ("Classic American Meal", 160, 4.6, "/static/images/Classic American Meal.png"),
        ("Fruit Platter", 100, 4.7, "/static/images/Fruit Platter.png"),
        ("Roast Meat", 210, 4.8, "/static/images/Roast Meat.png"),
        ("Prawn Noodles", 130, 4.7, "/static/images/Prawn Noodles.png"),
        ("Fruit Platter with Smoothie", 120, 4.8, "/static/images/Fruit Platter with Smoothie Bowl.png"),
        ("Thai Red Curry", 140, 4.6, "/static/images/Thai Red Curry.png"),
        ("Pizza with Bruschetta", 160, 4.7, "/static/images/Pizza with Bruschetta.png"),
    ],
    "Royal Feast": [
        ("Salmon Fillet", 230, 4.9, "/static/images/Salmon Fillet.png"),
        ("Burger with Fries", 110, 4.5, "/static/images/Burger with Fries.png"),
        ("Sponge Cake", 90, 4.4, "/static/images/Sponge Cake.png"),
        ("Fettuccine Carbonara", 120, 4.6, "/static/images/Fettuccine Carbonara.png"),
        ("Dumplings", 80, 4.5, "/static/images/Dumplings.png"),
        ("Red Velvet Cake", 120, 4.7, "/static/images/Red Velvet Cake.png"),
        ("Classic American Breakfast", 140, 4.7, "/static/images/Classic American Breakfast.png"),
        ("Chicken Biryani", 180, 4.8, "/static/images/Chicken Biryani.png"),
        ("Cupcakes", 80, 4.5, "/static/images/Cupcakes.png"),
        ("Papdi Chaat", 60, 4.4, "/static/images/Papdi Chaat.png"),
        ("Avocado and Egg Plate", 150, 4.8, "/static/images/Avocado and Egg Plate.png"),
    ],
    "Gourmet Lane": [
        ("Classic American Meal", 160, 4.6, "/static/images/Classic American Meal.png"),
        ("Fruit Platter", 100, 4.7, "/static/images/Fruit Platter.png"),
        ("Roast Meat", 210, 4.8, "/static/images/Roast Meat.png"),
        ("Prawn Noodles", 130, 4.7, "/static/images/Prawn Noodles.png"),
        ("Fruit Platter with Smoothie", 120, 4.8, "/static/images/Fruit Platter with Smoothie Bowl.png"),
        ("Thai Red Curry", 140, 4.6, "/static/images/Thai Red Curry.png"),
        ("Pizza with Bruschetta", 160, 4.7, "/static/images/Pizza with Bruschetta.png"),
        ("Salmon Fillet", 230, 4.9, "/static/images/Salmon Fillet.png"),
        ("Burger with Fries", 110, 4.5, "/static/images/Burger with Fries.png"),
        ("Sponge Cake", 90, 4.4, "/static/images/Sponge Cake.png"),
        ("Fettuccine Carbonara", 120, 4.6, "/static/images/Fettuccine Carbonara.png"),
        ("Dumplings", 80, 4.5, "/static/images/Dumplings.png"),
    ],
    "Tadka House": [
        ("Red Velvet Cake", 120, 4.7, "/static/images/Red Velvet Cake.png"),
        ("Chocolate Cake", 110, 4.6, "/static/images/Chocolate Cake.png"),
        ("Cupcakes", 80, 4.5, "/static/images/Cupcakes.png"),
        ("Papdi Chaat", 60, 4.4, "/static/images/Papdi Chaat.png"),
        ("Avocado and Egg Plate", 150, 4.8, "/static/images/Avocado and Egg Plate.png"),
        ("Classic American Breakfast", 140, 4.7, "/static/images/Classic American Breakfast.png"),
        ("Paniyaram", 70, 4.5, "/static/images/Paniyaram.png"),
        ("Pasta Salad", 100, 4.6, "/static/images/Pasta Salad.png"),
        ("Meleate Dosa", 90, 4.4, "/static/images/Meleate Dosa.png"),
        ("Masala Vada", 60, 4.3, "/static/images/Masala Vada.png"),
        ("Dosa", 80, 4.5, "/static/images/Dosa.png"),
    ],
    "Zaika Palace": [
        ("Chicken Biryani", 180, 4.8, "/static/images/Chicken Biryani.png"),
        ("Special Chicken Biryani", 200, 4.9, "/static/images/Special Chicken Biryani.png"),
        ("Laccha Paratha", 50, 4.2, "/static/images/Laccha Paratha.png"),
        ("Special Samosa", 40, 4.1, "/static/images/Special Samosa.png"),
        ("Special Idli", 60, 4.3, "/static/images/Special Idli.png"),
        ("Fruit Curd Rice", 90, 4.5, "/static/images/Fruit Curd Rice.png"),
        ("Mutton Biryani", 220, 4.9, "/static/images/Mutton Biryani.png"),
        ("Classic American Meal", 160, 4.6, "/static/images/Classic American Meal.png"),
        ("Fruit Platter", 100, 4.7, "/static/images/Fruit Platter.png"),
        ("Roast Meat", 210, 4.8, "/static/images/Roast Meat.png"),
        ("Prawn Noodles", 130, 4.7, "/static/images/Prawn Noodles.png"),
    ],
    "Bistro Bites": [
        ("Fruit Platter with Smoothie", 120, 4.8, "/static/images/Fruit Platter with Smoothie Bowl.png"),
        ("Thai Red Curry", 140, 4.6, "/static/images/Thai Red Curry.png"),
        ("Pizza with Bruschetta", 160, 4.7, "/static/images/Pizza with Bruschetta.png"),
        ("Salmon Fillet", 230, 4.9, "/static/images/Salmon Fillet.png"),
        ("Burger with Fries", 110, 4.5, "/static/images/Burger with Fries.png"),
        ("Sponge Cake", 90, 4.4, "/static/images/Sponge Cake.png"),
        ("Fettuccine Carbonara", 120, 4.6, "/static/images/Fettuccine Carbonara.png"),
        ("Dumplings", 80, 4.5, "/static/images/Dumplings.png"),
        ("Red Velvet Cake", 120, 4.7, "/static/images/Red Velvet Cake.png"),
        ("Classic American Breakfast", 140, 4.7, "/static/images/Classic American Breakfast.png"),
        ("Chicken Biryani", 180, 4.8, "/static/images/Chicken Biryani.png"),
    ],
    "Delight Kitchen": [
        ("Cupcakes", 80, 4.5, "/static/images/Cupcakes.png"),
        ("Papdi Chaat", 60, 4.4, "/static/images/Papdi Chaat.png"),
        ("Avocado and Egg Plate", 150, 4.8, "/static/images/Avocado and Egg Plate.png"),
        ("Classic American Breakfast", 140, 4.7, "/static/images/Classic American Breakfast.png"),
        ("Paniyaram", 70, 4.5, "/static/images/Paniyaram.png"),
        ("Pasta Salad", 100, 4.6, "/static/images/Pasta Salad.png"),
        ("Meleate Dosa", 90, 4.4, "/static/images/Meleate Dosa.png"),
        ("Masala Vada", 60, 4.3, "/static/images/Masala Vada.png"),
        ("Dosa", 80, 4.5, "/static/images/Dosa.png"),
        ("Chicken Biryani", 180, 4.8, "/static/images/Chicken Biryani.png"),
        ("Special Chicken Biryani", 200, 4.9, "/static/images/Special Chicken Biryani.png"),
    ],
    "Flavoursome Kitchen": [
        ("Laccha Paratha", 50, 4.2, "/static/images/Laccha Paratha.png"),
        ("Special Samosa", 40, 4.1, "/static/images/Special Samosa.png"),
        ("Special Idli", 60, 4.3, "/static/images/Special Idli.png"),
        ("Fruit Curd Rice", 90, 4.5, "/static/images/Fruit Curd Rice.png"),
        ("Mutton Biryani", 220, 4.9, "/static/images/Mutton Biryani.png"),
        ("Classic American Meal", 160, 4.6, "/static/images/Classic American Meal.png"),
        ("Fruit Platter", 100, 4.7, "/static/images/Fruit Platter.png"),
        ("Roast Meat", 210, 4.8, "/static/images/Roast Meat.png"),
        ("Prawn Noodles", 130, 4.7, "/static/images/Prawn Noodles.png"),
        ("Fruit Platter with Smoothie", 120, 4.8, "/static/images/Fruit Platter with Smoothie Bowl.png"),
        ("Thai Red Curry", 140, 4.6, "/static/images/Thai Red Curry.png"),
    ],
    "Gourmet Thali": [
        ("Pizza with Bruschetta", 160, 4.7, "/static/images/Pizza with Bruschetta.png"),
        ("Salmon Fillet", 230, 4.9, "/static/images/Salmon Fillet.png"),
        ("Burger with Fries", 110, 4.5, "/static/images/Burger with Fries.png"),
        ("Sponge Cake", 90, 4.4, "/static/images/Sponge Cake.png"),
        ("Fettuccine Carbonara", 120, 4.6, "/static/images/Fettuccine Carbonara.png"),
        ("Dumplings", 80, 4.5, "/static/images/Dumplings.png"),
        ("Red Velvet Cake", 120, 4.7, "/static/images/Red Velvet Cake.png"),
        ("Classic American Breakfast", 140, 4.7, "/static/images/Classic American Breakfast.png"),
        ("Chicken Biryani", 180, 4.8, "/static/images/Chicken Biryani.png"),
        ("Cupcakes", 80, 4.5, "/static/images/Cupcakes.png"),
        ("Papdi Chaat", 60, 4.4, "/static/images/Papdi Chaat.png"),
    ],
    "Magic Platter": [
        ("Avocado and Egg Plate", 150, 4.8, "/static/images/Avocado and Egg Plate.png"),
        ("Classic American Breakfast", 140, 4.7, "/static/images/Classic American Breakfast.png"),
        ("Paniyaram", 70, 4.5, "/static/images/Paniyaram.png"),
        ("Pasta Salad", 100, 4.6, "/static/images/Pasta Salad.png"),
        ("Meleate Dosa", 90, 4.4, "/static/images/Meleate Dosa.png"),
        ("Masala Vada", 60, 4.3, "/static/images/Masala Vada.png"),
        ("Dosa", 80, 4.5, "/static/images/Dosa.png"),
        ("Chicken Biryani", 180, 4.8, "/static/images/Chicken Biryani.png"),
        ("Special Chicken Biryani", 200, 4.9, "/static/images/Special Chicken Biryani.png"),
        ("Laccha Paratha", 50, 4.2, "/static/images/Laccha Paratha.png"),
        ("Special Samosa", 40, 4.1, "/static/images/Special Samosa.png"),
    ],
    "Kurry House": [
        ("Special Idli", 60, 4.3, "/static/images/Special Idli.png"),
        ("Fruit Curd Rice", 90, 4.5, "/static/images/Fruit Curd Rice.png"),
        ("Mutton Biryani", 220, 4.9, "/static/images/Mutton Biryani.png"),
        ("Classic American Meal", 160, 4.6, "/static/images/Classic American Meal.png"),
        ("Fruit Platter", 100, 4.7, "/static/images/Fruit Platter.png"),
        ("Roast Meat", 210, 4.8, "/static/images/Roast Meat.png"),
        ("Prawn Noodles", 130, 4.7, "/static/images/Prawn Noodles.png"),
        ("Fruit Platter with Smoothie", 120, 4.8, "/static/images/Fruit Platter with Smoothie Bowl.png"),
        ("Thai Red Curry", 140, 4.6, "/static/images/Thai Red Curry.png"),
        ("Pizza with Bruschetta", 160, 4.7, "/static/images/Pizza with Bruschetta.png"),
        ("Salmon Fillet", 230, 4.9, "/static/images/Salmon Fillet.png"),
    ],
    "Heritage House": [
        ("Burger with Fries", 110, 4.5, "/static/images/Burger with Fries.png"),
        ("Sponge Cake", 90, 4.4, "/static/images/Sponge Cake.png"),
        ("Fettuccine Carbonara", 120, 4.6, "/static/images/Fettuccine Carbonara.png"),
        ("Dumplings", 80, 4.5, "/static/images/Dumplings.png"),
        ("Red Velvet Cake", 120, 4.7, "/static/images/Red Velvet Cake.png"),
        ("Classic American Breakfast", 140, 4.7, "/static/images/Classic American Breakfast.png"),
        ("Chicken Biryani", 180, 4.8, "/static/images/Chicken Biryani.png"),
        ("Cupcakes", 80, 4.5, "/static/images/Cupcakes.png"),
        ("Papdi Chaat", 60, 4.4, "/static/images/Papdi Chaat.png"),
        ("Avocado and Egg Plate", 150, 4.8, "/static/images/Avocado and Egg Plate.png"),
        ("Classic American Meal", 160, 4.6, "/static/images/Classic American Meal.png"),
    ],
    "Royal Lane": [
        ("Fruit Platter", 100, 4.7, "/static/images/Fruit Platter.png"),
        ("Roast Meat", 210, 4.8, "/static/images/Roast Meat.png"),
        ("Prawn Noodles", 130, 4.7, "/static/images/Prawn Noodles.png"),
        ("Fruit Platter with Smoothie", 120, 4.8, "/static/images/Fruit Platter with Smoothie Bowl.png"),
        ("Thai Red Curry", 140, 4.6, "/static/images/Thai Red Curry.png"),
        ("Pizza with Bruschetta", 160, 4.7, "/static/images/Pizza with Bruschetta.png"),
        ("Salmon Fillet", 230, 4.9, "/static/images/Salmon Fillet.png"),
        ("Burger with Fries", 110, 4.5, "/static/images/Burger with Fries.png"),
        ("Sponge Cake", 90, 4.4, "/static/images/Sponge Cake.png"),
        ("Fettuccine Carbonara", 120, 4.6, "/static/images/Fettuccine Carbonara.png"),
        ("Dumplings", 80, 4.5, "/static/images/Dumplings.png"),
    ],
    "Chettinad Corner": [
        ("Red Velvet Cake", 120, 4.7, "/static/images/Red Velvet Cake.png"),
        ("Chocolate Cake", 110, 4.6, "/static/images/Chocolate Cake.png"),
        ("Cupcakes", 80, 4.5, "/static/images/Cupcakes.png"),
        ("Papdi Chaat", 60, 4.4, "/static/images/Papdi Chaat.png"),
        ("Avocado and Egg Plate", 150, 4.8, "/static/images/Avocado and Egg Plate.png"),
        ("Classic American Breakfast", 140, 4.7, "/static/images/Classic American Breakfast.png"),
        ("Paniyaram", 70, 4.5, "/static/images/Paniyaram.png"),
        ("Pasta Salad", 100, 4.6, "/static/images/Pasta Salad.png"),
        ("Meleate Dosa", 90, 4.4, "/static/images/Meleate Dosa.png"),
        ("Masala Vada", 60, 4.3, "/static/images/Masala Vada.png"),
        ("Dosa", 80, 4.5, "/static/images/Dosa.png"),
    ],
    "Darbar Dine": [
        ("Chicken Biryani", 180, 4.8, "/static/images/Chicken Biryani.png"),
        ("Special Chicken Biryani", 200, 4.9, "/static/images/Special Chicken Biryani.png"),
        ("Laccha Paratha", 50, 4.2, "/static/images/Laccha Paratha.png"),
        ("Special Samosa", 40, 4.1, "/static/images/Special Samosa.png"),
        ("Special Idli", 60, 4.3, "/static/images/Special Idli.png"),
        ("Fruit Curd Rice", 90, 4.5, "/static/images/Fruit Curd Rice.png"),
        ("Mutton Biryani", 220, 4.9, "/static/images/Mutton Biryani.png"),
        ("Classic American Meal", 160, 4.6, "/static/images/Classic American Meal.png"),
        ("Fruit Platter", 100, 4.7, "/static/images/Fruit Platter.png"),
        ("Roast Meat", 210, 4.8, "/static/images/Roast Meat.png"),
        ("Prawn Noodles", 130, 4.7, "/static/images/Prawn Noodles.png"),
    ],
    "Chefs Table": [
        ("Fruit Platter with Smoothie", 120, 4.8, "/static/images/Fruit Platter with Smoothie Bowl.png"),
        ("Thai Red Curry", 140, 4.6, "/static/images/Thai Red Curry.png"),
        ("Pizza with Bruschetta", 160, 4.7, "/static/images/Pizza with Bruschetta.png"),
        ("Salmon Fillet", 230, 4.9, "/static/images/Salmon Fillet.png"),
        ("Burger with Fries", 110, 4.5, "/static/images/Burger with Fries.png"),
        ("Sponge Cake", 90, 4.4, "/static/images/Sponge Cake.png"),
        ("Fettuccine Carbonara", 120, 4.6, "/static/images/Fettuccine Carbonara.png"),
        ("Dumplings", 80, 4.5, "/static/images/Dumplings.png"),
        ("Red Velvet Cake", 120, 4.7, "/static/images/Red Velvet Cake.png"),
        ("Classic American Breakfast", 140, 4.7, "/static/images/Classic American Breakfast.png"),
        ("Chicken Biryani", 180, 4.8, "/static/images/Chicken Biryani.png"),
    ],
    "Valley Kitchen": [
        ("Cupcakes", 80, 4.5, "/static/images/Cupcakes.png"),
        ("Papdi Chaat", 60, 4.4, "/static/images/Papdi Chaat.png"),
        ("Avocado and Egg Plate", 150, 4.8, "/static/images/Avocado and Egg Plate.png"),
        ("Classic American Breakfast", 140, 4.7, "/static/images/Classic American Breakfast.png"),
        ("Paniyaram", 70, 4.5, "/static/images/Paniyaram.png"),
        ("Pasta Salad", 100, 4.6, "/static/images/Pasta Salad.png"),
        ("Meleate Dosa", 90, 4.4, "/static/images/Meleate Dosa.png"),
        ("Masala Vada", 60, 4.3, "/static/images/Masala Vada.png"),
        ("Dosa", 80, 4.5, "/static/images/Dosa.png"),
        ("Chicken Biryani", 180, 4.8, "/static/images/Chicken Biryani.png"),
        ("Special Chicken Biryani", 200, 4.9, "/static/images/Special Chicken Biryani.png"),
    ],
    "Aroma House": [
        ("Laccha Paratha", 50, 4.2, "/static/images/Laccha Paratha.png"),
        ("Special Samosa", 40, 4.1, "/static/images/Special Samosa.png"),
        ("Special Idli", 60, 4.3, "/static/images/Special Idli.png"),
        ("Fruit Curd Rice", 90, 4.5, "/static/images/Fruit Curd Rice.png"),
        ("Mutton Biryani", 220, 4.9, "/static/images/Mutton Biryani.png"),
        ("Classic American Meal", 160, 4.6, "/static/images/Classic American Meal.png"),
        ("Fruit Platter", 100, 4.7, "/static/images/Fruit Platter.png"),
        ("Roast Meat", 210, 4.8, "/static/images/Roast Meat.png"),
        ("Prawn Noodles", 130, 4.7, "/static/images/Prawn Noodles.png"),
        ("Fruit Platter with Smoothie", 120, 4.8, "/static/images/Fruit Platter with Smoothie Bowl.png"),
        ("Thai Red Curry", 140, 4.6, "/static/images/Thai Red Curry.png"),
    ],
    "Delicacies Hub": [
        ("Pizza with Bruschetta", 160, 4.7, "/static/images/Pizza with Bruschetta.png"),
        ("Salmon Fillet", 230, 4.9, "/static/images/Salmon Fillet.png"),
        ("Burger with Fries", 110, 4.5, "/static/images/Burger with Fries.png"),
        ("Sponge Cake", 90, 4.4, "/static/images/Sponge Cake.png"),
        ("Fettuccine Carbonara", 120, 4.6, "/static/images/Fettuccine Carbonara.png"),
        ("Dumplings", 80, 4.5, "/static/images/Dumplings.png"),
        ("Red Velvet Cake", 120, 4.7, "/static/images/Red Velvet Cake.png"),
        ("Classic American Breakfast", 140, 4.7, "/static/images/Classic American Breakfast.png"),
        ("Chicken Biryani", 180, 4.8, "/static/images/Chicken Biryani.png"),
        ("Cupcakes", 80, 4.5, "/static/images/Cupcakes.png"),
        ("Papdi Chaat", 60, 4.4, "/static/images/Papdi Chaat.png"),
    ],
}
            restaurants = []
            for name, cuisine, rating, image_url in restaurant_data:
                r = Restaurant(name=name, cuisine=cuisine, rating=rating, image_url=image_url)
                db.session.add(r)
                restaurants.append(r)
            db.session.commit()

            # Food items assign karo naam se
            for r in restaurants:
                items = food_items_by_restaurant.get(r.name, [])
                for fname, price, rating, img in items:
                    item = MenuItem(
                        restaurant_id=r.id,
                        name=fname,
                        price=price,
                        rating=rating,
                        image_url=img
                    )
                    db.session.add(item)
            db.session.commit()
    app.run(debug=True)