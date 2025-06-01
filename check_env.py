import os
from dotenv import load_dotenv

load_dotenv()

required_vars = [
    "OPENAI_API_KEY",
    "MY_EMAIL",
    "PRESENTATION_ID",
    "TELEGRAM_BOT_TOKEN"
]

missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print("⚠️  Missing required environment variables:")
    for var in missing_vars:
        print(f"  - {var}")

    print("\nPlease add these to your .env file before running MarryMe.")
    print("Quick tips:")
    if "OPENAI_API_KEY" in missing_vars:
        print("- Get OpenAI API key from https://platform.openai.com/account/api-keys")
    if "MY_EMAIL" in missing_vars:
        print("- Your email to share access to generated proposals")
    if "PRESENTATION_ID" in missing_vars:
        print("- Google Slides template ID (from the URL of your slide deck)")
    if "TELEGRAM_BOT_TOKEN" in missing_vars:
        print("- Telegram Bot token from @BotFather on Telegram")

    exit(1)

print("✅ All required environment variables found. Ready to roll!")
