TOKEN = '7485059047:AAE7CKhFzx1uPhXQdUwKbA9cYDrrV7EhjO4'
import random
from telegram import Update
from telegram.ext import (Application,
                          CommandHandler,
                          ContextTypes,
                          MessageHandler,
                          ConversationHandler,
                          filters)
jokes = [
    "Колобок повесился",
    "— Я боюсь прыгать — вдруг парашют не раскроется? \n— Еще никто никогда не жаловался, что у него не раскрылся парашют.",
    "У канибала умер сын...  Грустно и вкусно.",
    "Когда я вижу вырезанные на деревьях имена влюбленных, я не нахожу это романтичным. Кошмарно, что люди ходят на свидания с ножами.",
    "Акробат умер на батуте, но еще какое-то время продолжал радовать публику.",
    "— Ура, я поступила в автошколу, скоро будет на одного пешехода меньше! \n — А может, и не на одного.",
]
facts = ['У осьминогов 3 сердца', 'В Египетских пирамидах использовалось подобие бетона',
         'Виноград взрывается в микроволновой печи', 'У блондинов больше волос', 'Кость в пять раз прочнее стали']
riddles = [("2+2", "4"), ("3*3*3*3", "273"), ('2^10', '1024'),
           ("Что уходит и никогда не возвращается?", "Время")]
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Привет! Я ваш новый бот. Я могу рассказать анекдоты, загадать загадки и поделиться интересными фактами. Используйте команды: "/joke", "/riddle", "/fact", "/start".')
    return ConversationHandler.END
async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(random.choice(jokes))
    return ConversationHandler.END
async def fact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(random.choice(facts))
    return ConversationHandler.END
RIDDLE, ANSWER = range(2)
async def riddle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    riddle, answer = random.choice(riddles)
    context.user_data['riddle_answer'] = answer
    await update.message.reply_text(f"Загадка: {riddle}")
    return RIDDLE
async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_answer = update.message.text
    correct_answer = context.user_data.get('riddle_answer')
    if user_answer.lower() == correct_answer.lower():
        await update.message.reply_text("Правильно!")
    else:
        await update.message.reply_text(f"Неправильно. Правильный ответ: {correct_answer}")
    return ConversationHandler.END
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("joke", joke))
    application.add_handler(CommandHandler("fact", fact))
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('riddle', riddle)],
        states={
            RIDDLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, answer)],
        },
        fallbacks=[],
    )
    application.add_handler(conv_handler)
    application.run_polling()
if name == 'main':
    main()


# Вводим в разработку