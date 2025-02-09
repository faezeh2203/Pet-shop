from app import db
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Cart, CartItem, Product

class Cart:
    @login_required
    def cart(self):
        """Display the user's shopping cart"""
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            return render_template('cart.html', cart_items=[])

        cart_items = CartItem.query.filter_by(cart_id=cart.id).all()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        
        return render_template('cart.html', cart_items=cart_items, total_price=total_price)


    @login_required
    def add_to_cart(self, product_id):
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()

        product = Product.query.get_or_404(product_id)

        cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()
        if cart_item:
            cart_item.quantity += 1
        else:
            cart_item = CartItem(cart_id=cart.id, product_id=product.id, quantity=1)
            db.session.add(cart_item)

        db.session.commit()
        flash('محصول به سبد خرید اضافه شد.', 'success')
        return redirect(url_for('cart'))

    @login_required
    def remove_from_cart(self, cart_item_id):
        cart_item = CartItem.query.get_or_404(cart_item_id)
        if cart_item.cart.user_id == current_user.id:
            db.session.delete(cart_item)
            db.session.commit()
            flash('محصول از سبد خرید حذف شد.', 'success')
        else:
            flash('شما مجاز به حذف این محصول نیستید.', 'danger')
        return redirect(url_for('cart'))

    @login_required
    def update_cart(self, cart_item_id, quantity):
        cart_item = CartItem.query.get_or_404(cart_item_id)
        if cart_item.cart.user_id == current_user.id:
            if quantity > 0:
                cart_item.quantity = quantity
                db.session.commit()
                flash('تعداد محصول با موفقیت به‌روزرسانی شد.', 'success')
            else:
                flash('تعداد باید بیشتر از صفر باشد.', 'danger')
        else:
            flash('شما مجاز به به‌روزرسانی این محصول نیستید.', 'danger')
        return redirect(url_for('cart'))
