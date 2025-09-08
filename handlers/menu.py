from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database.products import get_products
from database.db import add_to_cart, get_cart, add_order, get_orders, remove_from_cart, clear_cart 



# =========================
# Helper: Show Cart
# =========================
async def show_cart(query, user_id):
    """Render the user's cart view."""
    cart_items = get_cart(user_id)

    if not cart_items:
        await query.edit_message_text(
            "🛒 Your cart is empty.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Back", callback_data="MENU_BACK")]
            ])
        )
        return

    text = "🛒 Your Cart:\n\n"
    total = 0
    keyboard = []

    products = get_products()
    name_to_id = {name: pid for pid, name, price in products}

    for name, price, qty in cart_items:
        subtotal = price * qty
        total += subtotal
        text += f"{name} x {qty} = {subtotal} KES\n"

        product_id = name_to_id.get(name)
        if product_id:
            keyboard.append([
                InlineKeyboardButton(f"➕ {name}", callback_data=f"ADD_ONE_{product_id}"),
                InlineKeyboardButton(f"❌ {name}", callback_data=f"REMOVE_ONE_{product_id}")
            ])

    text += f"\n💰 Total: {total} KES"
    keyboard.append([InlineKeyboardButton("✅ Checkout", callback_data="CHECKOUT")])
    keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="MENU_BACK")])

    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))


# =========================
# Main Menu
# =========================
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send the main menu with buttons."""
    keyboard = [
        [InlineKeyboardButton("🛍️ Products", callback_data="MENU_PRODUCTS")],
        [InlineKeyboardButton("🛒 Cart", callback_data="MENU_CART")],
        [InlineKeyboardButton("📦 My Orders", callback_data="MENU_ORDERS")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text(
            "📋 Main Menu:\nChoose an option:",
            reply_markup=reply_markup,
        )
    elif update.callback_query:
        await update.callback_query.edit_message_text(
            "📋 Main Menu:\nChoose an option:",
            reply_markup=reply_markup,
        )


# =========================
# Handle Button Clicks
# =========================
async def handle_menu_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Show Products
    if data == "MENU_PRODUCTS":
        products = get_products()
        if not products:
            await query.edit_message_text("❌ No products available right now.")
            return

        text = "🛍️ Available Products:\n\n"
        keyboard = []

        for product_id, name, price in products:
            text += f"• {name} - KES {price}\n"
            keyboard.append([
                InlineKeyboardButton(f"➕ Add {name}", callback_data=f"ADD_TO_CART_{product_id}")
            ])

        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="MENU_BACK")])

        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    # Show Cart
    elif data == "MENU_CART":
        user_id = query.from_user.id
        await show_cart(query, user_id)

    # Checkout → Save order and clear cart
    elif data == "CHECKOUT":
        user_id = query.from_user.id
        cart_items = get_cart(user_id)

        if not cart_items:
            await query.edit_message_text("❌ Your cart is empty.")
            return

        items_text = ", ".join([f"{name} x{qty}" for name, price, qty in cart_items])
        total = sum(price * qty for name, price, qty in cart_items)

        # Save order
        add_order(user_id, items_text, total)

        # 🔥 Clear cart after order
        clear_cart(user_id)

        await query.edit_message_text(
            f"✅ Order placed!\n\n🛒 Items: {items_text}\n💰 Total: {total} KES\n\nStatus: Pending"
        )

    # Show Orders
    elif data == "MENU_ORDERS":
        user_id = query.from_user.id
        orders = get_orders(user_id)

        if not orders:
            await query.edit_message_text("📦 You have no orders yet.")
            return

        text = "📦 Your Orders:\n\n"
        for order_id, items, total, status in orders:
            text += f"🆔 {order_id} | {items} | 💰 {total} KES | 📌 {status}\n\n"

        await query.edit_message_text(text)

    # Back to main menu
    elif data == "MENU_BACK":
        await menu(update, context)

    # Add product to cart (from product list)
    elif data.startswith("ADD_TO_CART_"):
        product_id = int(data.replace("ADD_TO_CART_", ""))
        user_id = query.from_user.id
        add_to_cart(user_id, product_id)
        await query.answer("✅ Added to cart!")

    # Add one more (from cart)
    elif data.startswith("ADD_ONE_"):
        product_id = int(data.replace("ADD_ONE_", ""))
        user_id = query.from_user.id
        add_to_cart(user_id, product_id)
        await query.answer("✅ Added one more!")
        await show_cart(query, user_id)  # refresh cart

    # Remove one (from cart)
    elif data.startswith("REMOVE_ONE_"):
        product_id = int(data.replace("REMOVE_ONE_", ""))
        user_id = query.from_user.id
        removed = remove_from_cart(user_id, product_id)

        if removed:
            await query.answer("❌ Removed one item!")
        else:
            await query.answer("⚠️ Product not found in cart.")

        await show_cart(query, user_id)  # refresh cart


# =========================
# Register Handlers
# =========================
def register_menu_handler(application):
    """Register the /menu command and button callbacks."""
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CallbackQueryHandler(handle_menu_click))
