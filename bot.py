import logging
import os
import sys

import locationfeature
import timesfeature
import commandslistfeature
import datasourcefeature

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(bot, update):
    update.effective_message.reply_text(update.effective_message.text)

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def location(bot, update):

    bot.send_message(chat_id=update.message.chat_id, text="Make sure your location is turned on. For optimal results, use 'High Accuracy' mode.")
    
    # creating location button object
    location_keyboard = KeyboardButton(text="send_location",  request_location=True)
   
    # creating keyboard object
    custom_keyboard = [[location_keyboard]]
    
    reply_markup = ReplyKeyboardMarkup(custom_keyboard) 
    
    update.message.reply_text("Would you mind sharing your location with me?", reply_markup=reply_markup)

def getMosques(bot, update):

    lat = update.message.location.latitude
    lon = update.message.location.longitude

    closestMosques = locationfeature.getClosestMosques(lat, lon)

    count = 1

    for mosque in closestMosques:
        message_text = str(count) + '\n' + mosque
        bot.send_message(chat_id=update.message.chat_id, text=message_text, parse_mode="Markdown")
        count = count + 1

def getPrayertimes(bot, update, args):

    timesMessage = timesfeature.construct_schedule(args)
    bot.send_message(chat_id=update.message.chat_id, text=timesMessage, parse_mode="Markdown")


def getCommands(bot, update):
    message = commandslistfeature.readCommands()
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode="Markdown")

def getDataSourcesInfo(bot, update)):
    message = datasourcefeature.readSourceInformation()
    bot.send_message(chat_id=update.message.chat_id, text=message, parse_mode="Markdown")

# method for debuggung
def log(message):

    print(message)
    sys.stdout.flush()


if __name__ == "__main__":

    # Set these variable to the appropriate values
    TOKEN = os.environ["TELEGRAM_TOKEN"]
    NAME = os.environ["APP_NAME"]

    # Port is given by Heroku
    PORT = os.environ.get('PORT')

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Set up the Updater
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    # ADD HANDLERS
    
    #echo command
    #dp.add_handler(MessageHandler(Filters.text, echo))
    #dp.add_handler(error)

    # start command
    dp.add_handler(CommandHandler('start', start))

    # location command
    dp.add_handler(CommandHandler('location', location))
    dp.add_handler(MessageHandler(Filters.location, getMosques))

    # prayer times command.
    dp.add_handler(CommandHandler('pt', getPrayertimes, pass_args=True))

    # show commands command
    dp.add_handler(CommandHandler('commands', getCommands))

    # data source command
    dp.add_handler(CommandHandler('data', getDataSourcesInfo))

    # Start the webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    updater.idle()
