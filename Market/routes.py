from Market import app
from flask import render_template,redirect,url_for,flash,request
from Market.models import Item,User
from Market.forms import RegisterForm,LoginForm,AdditemForm,PurchaseItemForm,SellItemForm
from Market import db
from flask_login import login_user, logout_user, login_required,current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')
@app.route('/market',methods=['GET','POST'])
@login_required
def market():
    purchase_form=PurchaseItemForm()
    selling_form=SellItemForm()
    if request.method=="POST":
        purchased_item=request.form.get('purchased_item')
        p_item_object=Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"congratulations! You purchased {p_item_object.name} for {p_item_object.price}$" ,category="success")
            else:
                flash("unfortunately,You don't have enough money to purchase",category="danger")
        sold_item=request.form.get('sold_item')
        s_item_object=Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"congratulations! You sold {s_item_object.name} back to market" ,category="success")
            else:
                flash(f"something went wrong in seling {s_item_object.name}",category="danger")

        return redirect(url_for("market"))
    if request.method=="GET":
        items = Item.query.filter_by(owner=None)
        owned_items=Item.query.filter_by(owner=current_user.id)
        return render_template('market.html',items=items,purchase_form=purchase_form,owned_items=owned_items,selling_form=selling_form)
@app.route('/register',methods=['GET','POST'])
def register_page():
    form=RegisterForm()
    if form.validate_on_submit():
        user_to_create=User(username=form.username.data,emailaddress=form.emailaddress.data,password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account created succesfully!You are now logged in as {user_to_create.username}', category='success')
        return redirect(url_for('market'))
    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}',category='danger')

    return render_template('register.html',form=form)

@app.route('/login', methods=['GET','POST'])
def login_page():
    form=LoginForm()
    if form.validate_on_submit():
        attempted_user=User.query.filter_by(username=form.username.data).first()
        
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success!You are loggen in as {attempted_user.username}', category='success')
            return redirect(url_for('market'))
        else:
            flash('Username and password are not match ! Please try again',category='danger')
        

    return render_template('login.html',form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))

@app.route('/additems',methods=['GET','POST'])
@login_required
def additems_page():
    if current_user.username =='narendra':
        form=AdditemForm()
        if form.validate_on_submit():
            item_to_create=Item(name=form.name.data,price=form.price.data,barcode=form.barcode.data,description=form.description.data)
            db.session.add(item_to_create)
            db.session.commit()
            # return redirect(url_for('market'))
            flash("Item added Successfully",category="success")
        if form.errors !={}:
            for err_msg in form.errors.values():
                flash(f'There was an error with creating a user: {err_msg}',category='danger')
    else:
        flash("Sorry, You are not allowed to access that page!",category="danger")
        return redirect(url_for('market'))
    return render_template('additem.html',form=form)


@app.route('/clear_database', methods=['GET', 'POST'])
def clear_database():
    db.drop_all()
    db.create_all()
    return "Database cleared"