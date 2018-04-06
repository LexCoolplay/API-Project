from telegram.ext import ConversationHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters, MessageHandler
from telegram.ext import Updater

def start(bot, update):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живете?")

    # Это то число, которое является ключем в словаре states — втором параметре ConversationHandler'а.
    return 1
    # Оно указывает, что дальше на сообщения от этого пользователя должен отвечать обработчик states[1].
    # До этого момента обработчиков текстовых сообщений для этого пользователя не существовало,
    # поэтому текстовые сообщения игнорировались.

def first_response(bot, update, user_data):
    # Сохраняем ответ в словаре.
    user_data['locality'] = update.message.text
    update.message.reply_text(
        "Какая погода в городе {0}?".format(user_data['locality']))
    return 2


def second_response(bot, update, user_data):
    weather = update.message.text
    update.message.reply_text("Спасибо за участие в опросе! Привет, {0}!".
                              format(user_data['locality']))  # Используем user_data в ответе.
    return ConversationHandler.END

def stop(bot, update, user_data):
    return ConversationHandler.END


def main():
    updater = Updater("546913145:AAEYiORbmyB-yEyWzUIZkR4AGK3EROVpi34")

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        # Без изменений
        entry_points=[CommandHandler('start', start)],

        states={
            # Добавили user_data для сохранения ответа.
            1: [MessageHandler(Filters.text, first_response, pass_user_data=True)],
            # ...и для его использования.
            2: [MessageHandler(Filters.text, second_response, pass_user_data=True)]
        },

        # Без изменений
        fallbacks=[CommandHandler('stop', stop)]


    )

    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
