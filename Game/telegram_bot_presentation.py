import GameCore

from telegram.ext import CommandHandler
from telegram.ext import Updater


def telegram_decorator(func):
    def result_func(bot, update, args):
        response = func(*args)
        update.message.reply_text(response)
    return result_func


def main():
    updater = Updater("546913145:AAEYiORbmyB-yEyWzUIZkR4AGK3EROVpi34")

    logic = GameCore.Game()
    logic.load_data()

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("login", telegram_decorator(logic.log_in), pass_args=True))
    dp.add_handler(CommandHandler("register", telegram_decorator(logic.register), pass_args=True))
    dp.add_handler(CommandHandler("quest", telegram_decorator(logic.start_quest), pass_args=True))
    dp.add_handler(CommandHandler("forge", telegram_decorator(logic.forge), pass_args=True))

    updater.start_polling()

    updater.idle()
    logic.save_data()

if __name__ == '__main__':
    main()


