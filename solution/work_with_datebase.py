import sqlite3
import datetime
import re


error = -1
accept = 1
person_data_init = "id integer PRIMARY KEY, \
	user_id integer UNIQUE, \
	user_name text NOT NULL, \
	user_money_not_in_stocks integer, \
	competition_start date"

person_data_parametres = "user_id, \
	user_name, \
	user_money_not_in_stocks, \
	competition_start"

def sql_delete_table(table, name):
	cursor = table.cursor()
	cursor.execute('DROP table if exists {}'.format(name))
	table.commit()

def sql_create_table(table, name, parametres):
	sql_delete_table(table, name)

	cursor = table.cursor()
	cursor.execute("CREATE TABLE if not exists {}({})".format(name, parametres))
	table.commit()


def sql_connection():
	try:
		table = sqlite3.connect('person_info/data_person.db', check_same_thread=False)
		print('connection...: Database is created in memory')
		return table
	except Error:
		print(Error)


def db_table_val(table, name, user_id: int, user_name: str, personal_parametres: str,
	user_money_not_in_stocks=1000, competition_start=datetime.datetime(year=2013, month=9, day=11)):
	cursor = table.cursor()
	try:
		cursor.execute('INSERT INTO {} ({}) VALUES(?, ?, ?, ?)'.format(name, person_data_parametres), 
			(user_id, user_name, user_money_not_in_stocks, competition_start))
	except sqlite3.IntegrityError:
		return error
	table.commit()
	return accept


def was_reg(table, name, user_id: int):
	cursor = table.cursor()
	cursor.execute("SELECT user_id FROM {} WHERE user_id == {}".format(name, user_id))
	row = cursor.fetchall()
	if not len(row):
		return error
	return accept


def get_cost(table, name, user_id: int):
	cursor = table.cursor()
	cursor.execute("SELECT user_money_not_in_stocks FROM {} WHERE user_id == {}".format(name, user_id))
	row = cursor.fetchall()
	if not len(row):
		return error
	return int(re.search(r'\d+', str(row[0])).group(0))


def get_users(table, name):
	cursor = table.cursor()
	cursor.execute("SELECT user_id FROM {}".format(name))
	row = cursor.fetchall()
	list_id = re.findall(r'\d+', str(row))
	return [int(x) for x in list_id]


def init_rooms(table, name):
	for ith_name in name:
		sql_create_table(table, ith_name, person_data_init)