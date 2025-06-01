import check_env  # just run this; it will exit if vars missing
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from automation import parse_client_notes, extract_keys, authenticate_with_service_account, copy_presentation, give_me_access_to_file, replace_text_in_slides
from dotenv import load_dotenv
from dotenv import load_dotenv
import os
# Load your secret .env.local first (locks in secret vars)
load_dotenv(dotenv_path=".env.local")
# Then load user .env file (does NOT override existing vars)
load_dotenv(dotenv_path=".env", override=False)





TEMPLATE_ID = os.getenv('PRESENTATION_ID')
MY_EMAIL = os.getenv('MY_EMAIL')





async def handle_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    client_notes = update.message.text
    await update.message.reply_text("🧠 Got the notes! Generating proposal...")

    try:
        result = parse_client_notes(notes=client_notes)
        needed = ["client_name", "budget", "timeline", "goal", "extras"]
        client_data = extract_keys(result, needed)
        creds = authenticate_with_service_account()

        new_presentation_id = copy_presentation(
            template_id=TEMPLATE_ID,
            new_title=f"Proposal for {client_data.get('client_name', 'Client')}",
            credentials=creds
        )

        give_me_access_to_file(new_presentation_id, MY_EMAIL, creds)

        replace_text_in_slides(new_presentation_id, {
            f"{{{{{key}}}}}": "\n".join(value) if isinstance(value, list) else str(value)
            for key, value in client_data.items()
        }, creds)

        link = f"https://docs.google.com/presentation/d/{new_presentation_id}/edit"
        await update.message.reply_text(f"✅ Proposal ready: {link}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")





if __name__ == '__main__':
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_notes))

    print("🤖 Bot is running...")
    app.run_polling()
