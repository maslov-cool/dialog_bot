# Импортируем необходимые классы.
# @dialog_by_coding_lover_bot --> ник в тг
import logging
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters


# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)
BOT_TOKEN = '7652454044:AAH5_Mr4NL3zT2juywbi9L1hK_fksgHFLFs'


async def start(update, context):
    await update.message.reply_text('''👋 Привет! Давай познакомимся поближе.

Сколько тебе лет?  
(Напиши число)  
Если хочешь пропустить этот вопрос — отправь /skip  
Если хочешь закончить общение — отправь /stop
''')
    return 'AGE'


async def first_question(update, context):
    context.user_data['age'] = update.message.text
    await update.message.reply_text('''Теперь определимся с полом:
- Парень
- Девушка''')
    return 'SEX'


async def skip_first(update, context):
    await update.message.reply_text(f'''Тайна придает тебе загадочности... 🕵️''')
    await second_question(update, context)


async def second_question(update, context):
    context.user_data['sex'] = update.message.text
    await update.message.reply_text('''📍 Из какого ты города?''')
    return 'CITY'


async def skip_second(update, context):
    await update.message.reply_text(f'''Тайна придает тебе загадочности... 🕵️''')
    await third_question(update, context)


async def third_question(update, context):
    context.user_data['city'] = update.message.text
    await update.message.reply_text('''Как мне тебя называть? (Имя или ник)''')
    return 'NAME'


async def skip_third(update, context):
    await update.message.reply_text(f'''Тайна придает тебе загадочности... 🕵️''')
    await fourth_question(update, context)


async def fourth_question(update, context):
    context.user_data['name'] = update.message.text
    await update.message.reply_text('''Расскажи о себе и кого хочешь найти, чем предлагаешь заняться. 
Это поможет лучше подобрать тебе компанию.''')
    return 'DESCRIPTION'


async def skip_fourth(update, context):
    await update.message.reply_text(f'''Тайна придает тебе загадочности... 🕵️''')
    await fifth_question(update, context)


async def fifth_question(update, context):
    context.user_data['description'] = update.message.text
    await update.message.reply_text('''Теперь пришли фото 👍, его будут видеть другие пользователи.''')
    return 'PHOTO'


async def skip_fifth(update, context):
    await update.message.reply_text(f'''Тайна придает тебе загадочности... 🕵️''')
    await sixth_question(update, context)


async def sixth_question(update, context):
    photo = update.message.photo[-1]
    context.user_data['photo_file_id'] = photo.file_id
    await update.message.reply_text('''Так выглядит твоя анкета:''')
    await update.message.reply_photo(
        photo=context.user_data['photo_file_id'],
        caption=f'''{context.user_data['name']}, {context.user_data['age']}, {context.user_data['city']} – 
{context.user_data['description']}'''
        )
    return ConversationHandler.END  # Константа, означающая конец диалога.
    # Все обработчики из states и fallbacks становятся неактивными.


async def stop(update, context):
    await update.message.reply_text('''Всего доброго!''')
    return ConversationHandler.END


def main():
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        # Точка входа в диалог.
        # В данном случае — команда /start. Она задаёт первый вопрос.
        entry_points=[CommandHandler('start', start)],

        # Состояние внутри диалога.
        # Вариант с двумя обработчиками, фильтрующими текстовые сообщения.
        states={
            'AGE': [MessageHandler(filters.TEXT & ~filters.COMMAND, first_question), CommandHandler("skip", skip_first)],
            'SEX': [MessageHandler(filters.TEXT & ~filters.COMMAND, second_question), CommandHandler("skip", skip_second)],
            'CITY': [MessageHandler(filters.TEXT & ~filters.COMMAND, third_question), CommandHandler("skip", skip_third)],
            'NAME': [MessageHandler(filters.TEXT & ~filters.COMMAND, fourth_question), CommandHandler("skip", skip_fourth)],
            'DESCRIPTION': [MessageHandler(filters.TEXT & ~filters.COMMAND, fifth_question), CommandHandler("skip", skip_fifth)],
            'PHOTO': [MessageHandler(filters.PHOTO, sixth_question)]
        },

        # Точка прерывания диалога. В данном случае — команда /stop.
        fallbacks=[CommandHandler('stop', stop)]
    )

    application.add_handler(conv_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()


