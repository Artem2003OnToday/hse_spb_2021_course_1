import collections

from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater


class dialog_bot(object):
	def __init__(self, generator):
		self.updater = Updater(token="2132506762:AAEFLHpFn6GP44hNUcgIcaOepxDlGn7H2CA")
		handler = MessageHandler(Filters.text | Filters.command, self.handle_message)
		self.updater.dispatcher.add_handler(handler)
		self.handlers = collections.defaultdict(generator)

	def start(self):
		self.updater.start_polling()

	def handle_message(self, bot, update: Updater):
		print(update)
		print('Receiver', update.message)
		chat_id = update.message.chat_id
		if update.message.text == "/start":
			self.handlers.pop(chat_id, None)
		if chat_id in self.handlers:
			try:
				answer = self.hanlers[chat_id].send(update.message)
			except StopIteration:
				del self.handlers[chat_id]
				return self.handle_message(bot, update)
		else:
			answer = next(self.handlers[chat_id])

		print("answer: %r" % answer)
		bot.sendMessage(chat_id=chat_id, text=answer)


def dialog():
	answer = yield "yep, how are you?"


if __name__ == "__main__":
	botik = dialog_bot(dialog)
	botik.start()