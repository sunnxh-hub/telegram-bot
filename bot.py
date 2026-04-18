import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, MessageHandler,
    ContextTypes, filters
)

TOKEN = os.getenv("TOKEN")

ADMIN_ID = 123456789       # <-- TU ID (luego lo cambiamos)
GROUP_ID = -1001234567890  # <-- TU GRUPO (luego lo cambiamos)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰 Comprar acceso", callback_data="comprar")]
    ]

    await update.message.reply_text(
        "🔥 Bienvenido\n\nCompra acceso al grupo VIP",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# botón comprar
async def comprar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        "💳 Pago en cripto\n\n"
        "USDT (TRC20):\n"
        "TU_DIRECCION_AQUI\n\n"
        "📩 Envía captura del pago"
    )

# recibir comprobante
async def comprobante(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        user = update.effective_user

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,
            caption=f"💰 Pago de @{user.username}\nID: {user.id}"
        )

        await update.message.reply_text("✅ Comprobante enviado")

# dar acceso
async def dar_acceso(user_id, context):
    link = await context.bot.create_chat_invite_link(
        chat_id=GROUP_ID,
        member_limit=1
    )

    await context.bot.send_message(
        chat_id=user_id,
        text=f"✅ Acceso aprobado:\n{link.invite_link}"
    )

# comando aprobar
async def aprobar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = int(context.args[0])
    await dar_acceso(user_id, context)

    await update.message.reply_text("✅ Usuario aprobado")

# botones
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "comprar":
        await comprar(update, context)


# función para ver tu ID
async def ver_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("TU ID:", update.effective_user.id)


# app
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("aprobar", aprobar))
app.add_handler(CallbackQueryHandler(botones))
app.add_handler(MessageHandler(filters.PHOTO, comprobante))

# 👇 este sirve para mostrar tu ID en logs
app.add_handler(MessageHandler(filters.ALL, ver_id))

app.run_polling()