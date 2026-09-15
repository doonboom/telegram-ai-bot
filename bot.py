import os
from openai import AsyncOpenAI
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
Sen Agrobank Namangan hududiy AI yordamchisisan.

Foydalanuvchilarga o'zbek tilida sodda, hurmatli va aniq javob ber.
Savol rus tilida bo'lsa, rus tilida javob ber.
Bank kreditlari, bank xizmatlari va umumiy savollarga yordam ber.

Agar aniq bank sharti yoki rasmiy ma'lumot mavjud bo'lmasa,
taxminiy ma'lumotni fakt sifatida bermagin.
Kerak bo'lsa, foydalanuvchini bankning rasmiy manbasiga murojaat qilishga yo'naltir.

Kredit hisob-kitobida summa, foiz, muddat va annuitet kabi
parametrlarni hisobga ol.
"""

async def answer_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user_text = update.message.text.strip()

    # Buyruqlarni AI ga yubormaymiz
    if user_text.startswith("/"):
        return

    try:
        response = await client.responses.create(
            model="gpt-5.4-mini",
            instructions=SYSTEM_PROMPT,
            input=user_text,
            max_output_tokens=700,
        )

        answer = response.output_text.strip()

        if answer:
            await update.message.reply_text(answer)

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text(
            "Kechirasiz, hozir AI xizmatida vaqtinchalik muammo yuz berdi."
        )


def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            answer_message
        )
    )

    print("Agrobank AI bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()
