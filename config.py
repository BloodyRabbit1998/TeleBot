import json

with open('setting.json',"r") as file:
    conf_file=json.load(file)

BOT_TOKEN=conf_file['bot_token']

GPT_TOKEN=conf_file['gpt_token']

ADMINS=conf_file["admin_ids"]

PRICES=conf_file["prices"]

BANKNOTE=conf_file["banknote"]



