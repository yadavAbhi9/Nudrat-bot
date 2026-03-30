import random
import asyncio
import google.generativeai as genai

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction

# ===== API KEYS =====
API_KEYS = ["AIzaSyAnbGIJVsW-_VZL1fyUeUAPbAe9AG2ufCk",
"AIzaSyC2ynRpa7Ai0OVKuCobZ-QZhV0tNf9skWE",
"AIzaSyCwMhyqFewmoMI7MMt97icy9z3AtF5JYh8",
"AIzaSyDosSJceaMuMa7IIT0XpfcP_QnOn-zS02c",
"AIzaSyDPI-x_nRmsETRJ-jVNZbD6ZZ5QUqUXIiE",
"AIzaSyCz_OQ2yMlaEPBaWPkAsHXdZrCLcuWHn4g",
"AIzaSyAe7I0zDuaezQWSZLxo5wvioI_TIUoojSw",
"AIzaSyCkIp6Gl5dwa_jQARuffv47nrctUNjecyo",
"AIzaSyDERfzazxNW8ie_9OWIgyqDb_dQjpPHmpA",
"AIzaSyDKcm2OBkVdxDOMAQ7cyeUHMwdYHQII8sU",
"AIzaSyDoMaYbgbOlTEnjV8_oJ3zMkDxYf9PjSuc",
"AIzaSyBRFdTLuqE6Rsp2DRV7nwWH2kBAUCpHHPE",
"AIzaSyD10Nf2CNbGV20dMbF4fYen5trP0Jw0NZ8",
"AIzaSyALCDlltyvjLEGohyuqaS9zloYuFHdB1Gg",
"AIzaSyBt4VRlQDqJQtT0PrpcdT7PXVCmuleWp-o",
"AIzaSyBqBI1U5_qwwiGkN2gaz4OAKnApG41zanA",
"AIzaSyCNccDlxp-oXu5lbnVEfL9gc4NWpN0OgaQ",
"AIzaSyC13B4B63HFhR_ih28iLcvi96vbmbcQKWg",
"AIzaSyC6CThAX8hQ6zk1WnznO8tE-env_kIqwQ0",
"AIzaSyDK-Tm-Yem4frgf-KLvhwEtco5HMM59YKU",
"AIzaSyCinp-kWPW0SEjIx9ai0TjlXCM1CZAGL3w",
"AIzaSyBAJCtYBzJl187B1PD64a5EOG_4g0Av3Kc",
"AIzaSyBILN1HaruNJlZsfcj3QONW7pywoIaOD4c",
"AIzaSyCleENcgdzByU9Vtq4CPFs9A4JRnl3aJT0",
"AIzaSyAxf_lw0qPkkOijWBrKO3_PUvhQqJVT3R4",
"AIzaSyD2jATLjfUQv9UKyTmaEGISxJEdGOzPwcg",
"AIzaSyB9nh_XuFHI7pQQV_2LMWFwgxdTzyltNPQ",
"AIzaSyBVNPEeVfIHKHbZl_8OZGS-D5awzS9D9BE",
"AIzaSyBXvb5H8hoVUeqczD42zIPg43GpgWcYGSs",
"AIzaSyC5Yba-FOkiT9crjTXa-7h-6-3SYWTNsPU",
"AIzaSyAvdoGwFz3RD2fcx6203sfDP4zeI1aAs-w",
"AIzaSyAz0SJRqDnayWlRdFSuNL_ooXuKxumvslk",
"AIzaSyAUO9iHM1fwGd0oh5DEKvO4Fw_SXg92VMs",
"AIzaSyAX9YB2NOEGiNqv9CBDLx9mFY5YU604P8o",
"AIzaSyD7svPbv2se6Rw7R2FkZfGCrnLb0y8cg4s",
"AIzaSyDfOHuTJBBWbw-bjtztDpZOPKMF3LkZkx4"
]

# ===== MODEL =====
model = genai.GenerativeModel("gemini-2.5-flash")

# ===== MEMORY STORAGE =====
chat_memory = {}

# ===== PERSONALITY =====
personality = """
Your name is Nudrat.
You are a friendly girl chatting on Telegram.
Speak in Hindi + English mix.

Rules:
- Talk like a normal girl.
- Keep replies short and natural.
- Don't use jaan/baby every time.
"""

# ===== TYPING EFFECT =====
async def typing_effect(context, chat_id):
    for _ in range(5):   # typing duration increased
        await context.bot.send_chat_action(chat_id, ChatAction.TYPING)
        await asyncio.sleep(1)

# ===== CHAT FUNCTION =====
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await typing_effect(context, update.effective_chat.id)

    user_id = update.message.chat_id
    user_message = update.message.text

    # memory
    if user_id not in chat_memory:
        chat_memory[user_id] = []

    chat_memory[user_id].append(f"User: {user_message}")
    history = "\n".join(chat_memory[user_id][-5:])

    prompt = f"""
{personality}

Chat history:
{history}

Reply naturally.
"""

    reply = "Thoda network slow hai... 😅"

    for key in API_KEYS:
        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel("gemini-2.5-flash")

            response = model.generate_content(prompt)
            if response and response.text:
                reply = response.text
                break

        except Exception as e:
            print(e)
            continue

    chat_memory[user_id].append(f"Bot: {reply}")
    await update.message.reply_text(reply)

# ===== START =====
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await typing_effect(context, update.effective_chat.id)
    await update.message.reply_text("Hey... 😊 Mujhse baat karo")

# ===== MAIN =====
TELEGRAM_TOKEN = "8728299275:AAFRwJcu02hl_0pL7TiFDrSnibEgh4GcHvE"

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Bot running...")
app.run_polling(drop_pending_updates=True)