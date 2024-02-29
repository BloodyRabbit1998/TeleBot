import json
from dotenv import dotenv_values

env=dotenv_values(".env")  # take environment variables from .env.
with open('setting.json',"r") as file:
    conf_file=json.load(file)

URL_SQL=env["SQL_URL"]

BOT_TOKEN=env["BOT_TOKEN"]

GPT_TOKEN=env['GPT_TOKEN']

ADMINS=conf_file["admin_ids"]

PRICES=conf_file["prices"]

BANKNOTE=conf_file["banknote"]

STANDART_TIME=conf_file["standart"]["time"]
STANDART_DATE=conf_file["standart"]["date"]
