import work_with_datebase
import requests
import alpha_vantage
import json


# api=key: RC4ETG8NE4OBH2M6
API_URL = "https://www.alphavantage.co/query"
symbols = ['QCOM',"INTC","PDD"]
table_name = "stocks"

def get_stocks():
	for symbol in symbols:
		data = {
		"function": "TIME_SERIES_INTRADAY",
		"symbol": symbol,
		"interval" : "1min",
		"datatype": "json",
		"apikey": "RC4ETG8NE4OBH2M6"
		}

		response = requests.get(API_URL, data)
		data = response.json()

		print(symbol)
		a = data['Time Series (1min)']

		for key in a.keys():
			print(a[key]['2. high'] + " " + a[key]['3. low'] + " " + a[key]['5. volume'])


def init_stocks_table():
	return sql_connection()


def parse_stocks_to_database():
	pass
