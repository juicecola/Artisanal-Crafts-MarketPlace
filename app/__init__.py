import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from .forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from .db_models import db, User, Item
from dotenv import load_dotenv
from .admin.routes import admin

load_dotenv()
app = Flask(__name__)
app.register_blueprint(admin)

app.debug = True

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artisan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['STATIC_FOLDER'] = 'app/static'

Bootstrap(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

with app.app_context():
    db.create_all()

@app.context_processor
def inject_now():
    """ sends datetime to templates as 'now' """
    return {'now': datetime.utcnow()}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route("/")
def home():
    items = Item.query.all()
    return render_template("home.html", items=items)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user == None:
            flash(f'User with email {email} doesn\'t exist!<br> <a href={url_for("register")}>Register now!</a>', 'error')
            return redirect(url_for('login'))
        elif check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Email and password incorrect!!", "error")
            return redirect(url_for('login'))
    return render_template("login.html", form=form)

@app.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash(f"User with email {user.email} already exists!!<br> <a href={url_for('login')}>Login now!</a>", "error")
            return redirect(url_for('register'))
        new_user = User(name=form.name.data,
                        email=form.email.data,
                        password=generate_password_hash(
                                    form.password.data,
                                    method='pbkdf2:sha256',
                                    salt_length=8),
                        phone=form.phone.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Thanks for registering! You may login now.', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/add/<id>", methods=['POST'])
def add_to_cart(id):
    if not current_user.is_authenticated:
        flash(f'You must login first!<br> <a href={url_for("login")}>Login now!</a>', 'error')
        return redirect(url_for('login'))

    item = Item.query.get(id)
    if request.method == "POST":
        quantity = request.form["quantity"]
        current_user.add_to_cart(id, quantity)
        flash(f'''{item.name} successfully added to the <a href=cart>cart</a>.<br> <a href={url_for("cart")}>view cart!</a>''','success')
        return redirect(url_for('home'))

@app.route("/cart")
@login_required
def cart():
    price = 0
    price_ids = []
    items = []
    quantity = []
    for cart in current_user.cart:
        items.append(cart.item)
        quantity.append(cart.quantity)
        price_id_dict = {
            "price": cart.item.price_id,
            "quantity": cart.quantity,
        }
        price_ids.append(price_id_dict)
        price += cart.item.price * cart.quantity
    return render_template('cart.html', items=items, price=price, price_ids=price_ids, quantity=quantity)

@app.route('/orders')
@login_required
def orders():
    return render_template('orders.html', orders=current_user.orders)

@app.route("/remove/<id>/<quantity>")
@login_required
def remove(id, quantity):
    current_user.remove_from_cart(id, quantity)
    return redirect(url_for('cart'))

@app.route('/item/<int:id>')
def item(id):
    item = Item.query.get(id)
    return render_template('item.html', item=item)

@app.route('/search')
def search():
    query = request.args['query']
    search = "%{}%".format(query)
    items = Item.query.filter(Item.name.like(search)).all()
    return render_template('home.html', items=items, search=True, query=query)

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
	data = json.loads(request.form['price_ids'].replace("'", '"'))
	try:
		checkout_session = stripe.checkout.Session.create(
			client_reference_id=current_user.id,
			line_items=data,
			payment_method_types=[
			  'card',
			],
			mode='payment',
			success_url=url_for('payment_success', _external=True),
			cancel_url=url_for('payment_failure', _external=True),
		)
	except Exception as e:
		return str(e)
	return redirect(checkout_session.url, code=303)

if __name__ == "__main__":
    app.run()

