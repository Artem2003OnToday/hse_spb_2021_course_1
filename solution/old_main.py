from work_with_datebase import *
import telebot
import get_stocks
import datetime
import collections

bot_token = "2132506762:AAEFLHpFn6GP44hNUcgIcaOepxDlGn7H2CA"
bot = telebot.TeleBot(bot_token)

table = sql_connection()
person_data = "players"
sql_create_table(table, person_data, person_data_init)

rooms = ['A', 'B', 'C']
init_rooms(table, rooms)

@bot.message_handler(content_types=['text'])
def start(message):
	if message.text == "/start":
		bot.send_message(message.from_user.id, "Добро пожаловать в Stocks Doll. \
												Мы рады видеть всех, кто хочет посоревноваться с друзьями в успехах на бирже. \
												Зарегистрируйся, написав '/reg' и получи 1000 виртуальных долларов.")
	elif message.text == "/reg":
		us_id = message.from_user.id
		us_name = message.from_user.first_name

		if db_table_val(table, person_data, us_id, us_name, person_data_parametres) == error:
			bot.send_message(message.from_user.id, "Ты уже зарегистрирован. Зачем ты пытаешься сломать мою БД?")
		else:
			bot.send_message(message.from_user.id, "Ты попал в нашу ловушку, удачи!")
	elif message.text == '/cost':
		result = get_cost(table, person_data, message.from_user.id)
		if result == error:
			bot.send_message(message.from_user.id, "Для начала попробуй зарегистрироваться. Для этого напиши '/help' и найди там нужную команду.")
		else:
			bot.send_message(message.from_user.id, "На данный момент твоё состояние: " + str(result) + "$")
	elif message.text == '/help':
		bot.send_message(message.from_user.id, "Справочник по использованию Stocks(не Sex) Doll: \n\
												    /start - начало работы бота. \n\
												    /reg   - регистрация(ничего писать не надо, он сам вытянет всю информацию из вашего тг-аккаунта. \n\
												    /cost  - запрос для получения баланса\n")
	elif message.text == '/find_competition':
		if was_reg(table, person_data, message.from_user.id) == error:
			bot.send_message(message.from_user.id, "really? Ты не зарегистрирован. Надо бы...")
			return

		competitoin_users = []
		users = get_users(table, person_data)
		for ith_user in users:
			if message.from_user.id == ith_user:
				continue

			bot.send_message(ith_user, "Хотите ли вы поучавствовать в соревновании на бирже?")
			if message.text == '/ok' or message.text == '/yep':
				bot.send_message(ith_user, "Ты добавлен в комнату A")
			else:
				pass
	else:
		bot.send_message(message.from_user.id, "Я такое не умею:(")


bot.polling(none_stop=True, interval=0)