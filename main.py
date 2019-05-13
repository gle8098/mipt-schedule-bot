from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from logger import Logger
from database import BotDatabase
from Schedule import Schedule
from SecretToken import TOKEN
import locale


class ScheduleBot:
    _updater = None
    _schedule = None
    _database = None

    def init(self):
        self._updater = Updater(token=TOKEN, use_context=True)
        self._schedule = Schedule()
        self._database = BotDatabase()
        self._database.init()
        Logger.init()

        dispatcher = self._updater.dispatcher
        handler = CommandHandler('start', self.on_start_cmd)
        dispatcher.add_handler(handler)

        handler = MessageHandler(Filters.text, self.on_text)
        dispatcher.add_handler(handler)

        handler = CommandHandler('print', self.on_print_cmd)
        dispatcher.add_handler(handler)

        handler = CommandHandler('clear', self.on_clear_cmd)
        dispatcher.add_handler(handler)

    def _send_message(self, update, context, text):
        context.bot.send_message(chat_id=update.message.chat_id, text=text)

    def on_start_cmd(self, update, context):
        self._send_message(update, context, locale.TEXT_START_CMD)

    def on_text(self, update, context):
        chat_text = update.message.text
        groups = self._schedule.find_alike_groups(chat_text)
        if groups['count'] != 1:
            # Print similar groups
            self._send_message(update, context, groups['text'])
        else:
            # Set given group
            self._database.set_group(update.message.chat_id, chat_text)

            response = locale.TEXT_GROUP_SET.format(chat_text)
            self._send_message(update, context, response)

    def on_print_cmd(self, update, context):
        res = self._database.get_group(update.message.chat_id)
        if res is None:
            self._send_message(update, context, locale.TEXT_NO_GROUP_SET)
        else:
            response = self._schedule.get_schedule_weekly(res)
            self._send_message(update, context, response)

    def on_clear_cmd(self, update, context):
        self._database.del_group(update.message.chat_id)
        self._send_message(update, context, locale.TEXT_GROUP_CLEANED)

    def run(self):
        self._updater.start_polling()


if __name__ == "__main__":
    bot = ScheduleBot()
    bot.init()
    bot.run()
