import logging
from apscheduler.schedulers.background import BlockingScheduler
from telegram import Bot
from telegram.ext import CommandHandler, Updater
import requests
import random

TOKEN = "AQUI_VA_TU_TOKEN"

def start(update, context):
    update.message.reply_text("Hola senpai~ dime /img waifu nombre_personaje para traerte una waifu~")

def waifu(update, context):
    if len(context.args) == 0:
        update.message.reply_text("¿Waifu de quién? Usa: /img waifu nombre")
        return

    nombre = "_".join(context.args)
    urls = [
        f"https://api.waifu.pics/sfw/waifu",
        f"https://api.waifu.im/search/?included_tags={nombre}",
    ]

    for url in urls:
        try:
            r = requests.get(url)
            if r.status_code == 200:
                data = r.json()
                if "url" in data:
                    update.message.reply_photo(data["url"])
                    return
                elif "images" in data and data["images"]:
                    update.message.reply_photo(data["images"][0]["url"])
                    return
        except Exception as e:
            logging.error(str(e))

    update.message.reply_text("No encontré waifus de ese nombre, nyan~")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("img", waifu))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
