import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es"),
            InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
        ],
        [
            InlineKeyboardButton("🇧🇷 Português", callback_data="lang_pt"),
            InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang_tr")
        ],
        [
            InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de"),
            InlineKeyboardButton("🇫🇷 Français", callback_data="lang_fr")
        ]
    ]

    await update.message.reply_text(
        "✨ Welcome! Select your language:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# MENÚ PRINCIPAL
async def menu_principal(query):
    keyboard = [
        [InlineKeyboardButton("⚡ Comprar Acceso Instantáneo", callback_data="comprar")],
        [InlineKeyboardButton("👥 Comprar Acceso Grupo", callback_data="grupo")],
        [
            InlineKeyboardButton("📋 Menú", callback_data="menu"),
            InlineKeyboardButton("🎧 Soporte Humano", callback_data="soporte")
        ]
    ]

    await query.edit_message_text(
        "✨ ¿Qué le gustaría hacer?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# TIERS
async def menu_tiers(query):
    keyboard = [
        [
            InlineKeyboardButton("⭐ Tier Starter", callback_data="tier_starter"),
            InlineKeyboardButton("⭐ Tier 1", callback_data="tier1")
        ],
        [
            InlineKeyboardButton("⭐ Tier 2", callback_data="tier2"),
            InlineKeyboardButton("⭐ Tier 3", callback_data="tier3")
        ],
        [
            InlineKeyboardButton("⭐ Tier 4", callback_data="tier4"),
            InlineKeyboardButton("⭐ Tier 5", callback_data="tier5")
        ],
        [
            InlineKeyboardButton("⭐ Tier 6", callback_data="tier6"),
            InlineKeyboardButton("⭐ Tier Max", callback_data="tiermax")
        ],
        [InlineKeyboardButton("⭐ Extras", callback_data="extras")],
        [InlineKeyboardButton("🔙 Volver", callback_data="volver_menu")]
    ]

    await query.edit_message_text(
        "🎯 Seleccione el plan perfecto para usted:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# DETALLE
async def mostrar_tier(query):
    keyboard = [
        [InlineKeyboardButton("🛒 Comprar", callback_data="pagar")],
        [InlineKeyboardButton("🔙 Volver", callback_data="comprar")]
    ]

    await query.edit_message_text(
        "⭐ Tier Starter\n\n✔ Beneficio 1\n✔ Beneficio 2\n✔ Beneficio 3\n\n💰 $9500",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# PAGOS
async def metodos_pago(query):
    keyboard = [
        [InlineKeyboardButton("🎁 Vouchers", callback_data="voucher")],
        [InlineKeyboardButton("🔗 Criptomonedas", callback_data="crypto")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancelar")]
    ]

    await query.edit_message_text(
        "💳 Elija método de pago:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# CRIPTOS
async def criptos(query):
    keyboard = [
        [
            InlineKeyboardButton("₿ Bitcoin", callback_data="btc"),
            InlineKeyboardButton("Ξ Ethereum", callback_data="eth")
        ],
        [
            InlineKeyboardButton("Ł Litecoin", callback_data="ltc"),
            InlineKeyboardButton("₮ Tether", callback_data="usdt")
        ],
        [
            InlineKeyboardButton("◎ Solana", callback_data="sol"),
            InlineKeyboardButton("ɱ Monero", callback_data="xmr")
        ],
        [
            InlineKeyboardButton("✕ Ripple", callback_data="xrp"),
            InlineKeyboardButton("BNB", callback_data="bnb")
        ],
        [InlineKeyboardButton("🔙 Volver", callback_data="pagar")],
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancelar")]
    ]

    await query.edit_message_text(
        "📈 Elija criptomoneda:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# BOTONES
async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data.startswith("lang"):
        await menu_principal(query)

    elif data == "comprar":
        await menu_tiers(query)

    elif data.startswith("tier"):
        await mostrar_tier(query)

    elif data == "pagar":
        await metodos_pago(query)

    elif data == "crypto":
        await criptos(query)

    elif data == "volver_menu":
        await menu_principal(query)

    elif data == "cancelar":
        await query.edit_message_text("❌ Operación cancelada")

# MAIN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(botones))

app.run_polling()