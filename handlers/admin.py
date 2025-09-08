from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from database.db import get_orders, add_order  # you already have get_orders
import sqlite3

# =========================
# Config
# =========================
ADMIN_IDS = [8343894255]  # replace with your Telegram user ID(s)


# =========================
# Admin Menu
# =========================
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ You are not authorized to use this command.")
        return

    keyboard = [
        [InlineKeyboardButton("📦 View All Orders", callback_data="ADMIN_VIEW_ORDERS")],
        [InlineKeyboardButton("⬅️ Back to Main", callback_data="MENU_BACK")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("⚙️ Admin Panel:", reply_markup=reply_markup)


# =========================
# Handle Admin Actions
# =========================
async def handle_admin_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id

    if user_id not in ADMIN_IDS:
        await query.answer("❌ Not authorized")
        return

    data = query.data

    # View all orders
    if data == "ADMIN_VIEW_ORDERS":
        conn = sqlite3.connect("shop.db")
        cur = conn.cursor()
        cur.execute("SELECT id, user_id, items, total, status FROM orders ORDER BY id DESC")
        rows = cur.fetchall()
        conn.close()

        if not rows:
            await query.edit_message_text("📦 No orders yet.")
            return

        text = "📦 All Orders:\n\n"
        keyboard = []
        for oid, uid, items, total, status in rows:
            text += f"🆔 {oid} | 👤 User: {uid}\n{items}\n💰 {total} KES | 📌 {status}\n\n"
            keyboard.append([
                InlineKeyboardButton(f"✅ Mark {oid} Done", callback_data=f"ADMIN_MARK_DONE_{oid}"),
                InlineKeyboardButton(f"❌ Cancel {oid}", callback_data=f"ADMIN_CANCEL_{oid}")
            ])

        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="MENU_BACK")])
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    # Mark order as completed
    elif data.startswith("ADMIN_MARK_DONE_"):
        oid = int(data.replace("ADMIN_MARK_DONE_", ""))
        conn = sqlite3.connect("shop.db")
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status = 'Completed' WHERE id=?", (oid,))
        conn.commit()
        conn.close()
        await query.answer(f"✅ Order {oid} marked as completed")
        await handle_admin_click(update, context)  # refresh orders

    # Cancel order
    elif data.startswith("ADMIN_CANCEL_"):
        oid = int(data.replace("ADMIN_CANCEL_", ""))
        conn = sqlite3.connect("shop.db")
        cur = conn.cursor()
        cur.execute("UPDATE orders SET status = 'Cancelled' WHERE id=?", (oid,))
        conn.commit()
        conn.close()
        await query.answer(f"❌ Order {oid} cancelled")
        await handle_admin_click(update, context)  # refresh orders


# =========================
# Register Handlers
# =========================
def register_admin_handler(application):
    application.add_handler(CommandHandler("admin", admin))
    application.add_handler(CallbackQueryHandler(handle_admin_click, pattern="^ADMIN_"))
