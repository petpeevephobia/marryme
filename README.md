# MarryMe Proposal Assistant

## What is MarryMe?
MarryMe is a Telegram bot that automates creating personalized proposal decks from client notes. It uses Google Slides templates, OpenAI GPT parsing, and your Telegram bot for interaction.

---

## Setup

1. Copy `.env.example` to `.env`
2. Fill in your editable variables in `.env`:
   - OPENAI_API_KEY
   - MY_EMAIL
   - PRESENTATION_ID
   - TELEGRAM_BOT_TOKEN

---

## Prepare Your Google Slides Proposal Deck

1. Create a Google Slides template deck that MarryMe will duplicate and fill with client info.

2. Make sure your slide deck contains these **text placeholders exactly** (case-sensitive):

- `{{client_name}}`
- `{{budget}}`
- `{{timeline}}`
- `{{goal}}`
- `{{extras}}`

MarryMe will replace these placeholders with data extracted from client notes.

---

## Running MarryMe

1. Start your Telegram bot via "boy.py" OR host the code on Fly.io.
2. Send raw client notes to your Telegram bot. The notes must include the client business name and client email.
3. The bot will generate a proposal, duplicate your Google Slides template, fill in details, and reply with the proposal link.

---

## Notes

- MarryMe was never intended to be scalable. It was made specially for my AI-powered web agency, Solvia.

---

## Contact & Support

Reach out at solviapteltd@gmail.com (placeholder email) if you want help customizing or scaling MarryMe.
