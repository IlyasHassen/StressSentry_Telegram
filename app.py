import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ConversationHandler,
    MessageHandler, filters
)

from userdata import UserDataManager
from oura_client import OuraClient
from cohere_client import CohereClient
from bot_handlers import BotHandlers, AGENDA, EXAM, RESSENTI

def main():
    load_dotenv()

    dm = UserDataManager()
    oura = OuraClient()
    coh = CohereClient()
    handlers = BotHandlers(dm, oura, coh)

    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

    # Commandes simples
    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("journal", handlers.journal))
    app.add_handler(CommandHandler("oura_ring_4j", handlers.oura_ring_4j))
    app.add_handler(CommandHandler("recherche", handlers.recherche))
    app.add_handler(CommandHandler("organisation", handlers.organisation))
    app.add_handler(CommandHandler("delete", handlers.delete))

    # Conversations
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("agenda", handlers.agenda_start)],
        states={AGENDA: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.agenda_save)]},
        fallbacks=[]
    ))
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("exam", handlers.exam_start)],
        states={EXAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.exam_save)]},
        fallbacks=[]
    ))
    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("ressenti", handlers.ressenti_start)],
        states={RESSENTI: [MessageHandler(filters.TEXT & ~filters.COMMAND, handlers.ressenti_save)]},
        fallbacks=[]
    ))

    print("Bot démarré.")
    app.run_polling()

if __name__ == "__main__":
    main()
