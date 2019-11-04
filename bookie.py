#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)

class BookReadHelper():
    
    def start(self, update, context):
        reply_keyboard = [['Upload', 'Mine', "Others"]]
    
        self.chat_id = update.effective_chat.chat_id
        self.bot = update.effective_chat
        
        update.message.reply_text(
            'Hi! My name is Professor Bot. I will hold a conversation with you. '
            'Send /cancel to stop talking to me.\n\n'
            'Are you a boy or a girl?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
        return GENDER    
    
    def gender(self, update, context):
        user = update.message.from_user
        logger.info("Gender of %s: %s", user.first_name, update.message.text)
        update.message.reply_text('I see! Please send me a photo of yourself, '
                                  'so I know what you look like, or send /skip if you don\'t want to.',
                                  reply_markup=ReplyKeyboardRemove())
    
        return PHOTO
    
    
    def photo(self, update, context):
        user = update.message.from_user
        photo_file = update.message.photo[-1].get_file()
        photo_file.download('user_photo.jpg')
        logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
        update.message.reply_text('Gorgeous! Now, send me your location please, '
                                  'or send /skip if you don\'t want to.')
    
        return LOCATION
    
    
    def skip_photo(self, update, context):
        user = update.message.from_user
        logger.info("User %s did not send a photo.", user.first_name)
        update.message.reply_text('I bet you look great! Now, send me your location please, '
                                  'or send /skip.')
    
        return LOCATION
    
    def schedule(self, update, context):
        user = update.message.from_user
        logger.info(f'')
        # TODO: Parse schedule and store in DB
    
    def location(self, update, context):
        user = update.message.from_user
        user_location = update.message.location
        logger.info("Location of %s: %f / %f", user.first_name, user_location.latitude,
                    user_location.longitude)
        update.message.reply_text('Maybe I can visit you sometime! '
                                  'At last, tell me something about yourself.')
    
        return BIO

    def skip_location(self, update, context):
        user = update.message.from_user
        logger.info("User %s did not send a location.", user.first_name)
        update.message.reply_text('You seem a bit paranoid! '
                                  'At last, tell me something about yourself.')
    
        return BIO
    
    
    def bio(self, update, context):
        user = update.message.from_user
        logger.info("Bio of %s: %s", user.first_name, update.message.text)
        update.message.reply_text('Thank you! I hope we can talk again some day.')
    
        return ConversationHandler.END
    
    
    def cancel(self, update, context):
        user = update.message.from_user
        logger.info("User %s canceled the conversation.", user.first_name)
        update.message.reply_text('Bye! I hope we can talk again some day.',
                                  reply_markup=ReplyKeyboardRemove())
    
        return ConversationHandler.END
    
    
    def error(self, update, context):
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)
    
    
    def main(self):
        TOKEN = os.getenv('TOKEN')
        print(TOKEN)
        updater = Updater(TOKEN, use_context=True)
    
        dp = updater.dispatcher
    
        # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states = {
                GENDER: [MessageHandler(Filters.regex('^(Upload|My Books|Free Books)$'), self.gender)],
                PHOTO: [MessageHandler(Filters.photo, self.photo), CommandHandler('skip', self.skip_photo)],
                LOCATION: [MessageHandler(Filters.location, self.location), CommandHandler('skip', self.skip_location)],
                BIO: [MessageHandler(Filters.text, self.bio)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )
    
        dp.add_handler(conv_handler)
    
        dp.add_error_handler(self.error)
        updater.start_polling()
        updater.idle()
    
    def send_part(self):
        self.bot.send_message(chat_id=self.chat_id, text="I'm sorry Dave I'm afraid I can't do that.")

if __name__ == '__main__':
    brh = BookReadHelper()
    brh.main()
