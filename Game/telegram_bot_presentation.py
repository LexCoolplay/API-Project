import GameCore

from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram.ext import ConversationHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler


def telegram_decorator(func):
    def result_func(bot, update, user_data, args):
        response = func(user_data, *args)
        if type(response) == tuple:
            response = response[0]
        update.message.reply_text(response)
        return response
    return result_func


def conversation_decorator(func, **kwargs):
    if 'pass_args' in kwargs.keys() and kwargs['pass_args']:
        def result_conversation_func(bot, update, user_data, args):
            response = func(bot, update, user_data, args)
            print(response)
            return response
    else:
        def result_conversation_func(bot, update, user_data):
            response = func(bot, update, user_data)
            print(response)
            return response
    return result_conversation_func


def stop(bot, update):
    return ConversationHandler.END

def start(bot, update):
    update.message.reply_text(
        "I'm a game bot.\n" +
        "I can provide you with these functions:\n" +
        "/register <user>  <password> - create a new character(you will need to login manually)\n" +
        "/login <user>  <password> - login into your character profile\n" +
        "/info - provide info about your current character\n" +
        "/quest <quest_name> - start a quest.\n" +
        "Quest is a one-turn mission where you will face a monster with same level us you. " +
        "If you win you will recieve level and a part of equipment. " +
        "Else you will lose a level."
    )

def show_pic(bot, update, job_queue, chat_data, args):
    delay = int(args[0])
    job = job_queue.run_once(task, delay, context=update.message.chat_id)

    chat_data['job'] = job

    update.message.reply_text('Вернусь через ' + str(delay) + ' секунд!')



def main():
    updater = Updater("546913145:AAEYiORbmyB-yEyWzUIZkR4AGK3EROVpi34")

    logic = GameCore.Game()
    logic.load_data()

    print(conversation_decorator(logic.start_quest, pass_args=True, pass_user_data=True))
    quest_conversation = ConversationHandler(
        entry_points=[CommandHandler('quest', conversation_decorator(logic.start_quest, pass_args=True),
                                     pass_args=True, pass_user_data=True)],

        states={
            1: [MessageHandler(Filters.text,
                               conversation_decorator(logic.ask_trade_telegram_conversation_question_first_response),
                               pass_user_data=True)],
            2: [MessageHandler(Filters.text,
                               conversation_decorator(logic.ask_trade_telegram_conversation_question_second_response),
                               pass_user_data=True)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("login", telegram_decorator(logic.log_in),
                                  pass_args=True, pass_user_data=True))
    dp.add_handler(CommandHandler("register", telegram_decorator(logic.register),
                                  pass_args=True, pass_user_data=True))
    dp.add_handler(CommandHandler("forge", telegram_decorator(logic.forge),
                                  pass_args=True, pass_user_data=True))
    dp.add_handler(quest_conversation)
    dp.add_handler(CommandHandler("info", telegram_decorator(logic.get_character_info),
                                  pass_args=True, pass_user_data=True))
    dp.add_handler(CommandHandler('start', start))
    updater.start_polling()

    updater.idle()
    logic.save_data()

if __name__ == '__main__':
    main()


