from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import InputMediaPhoto
import cfg, utils

updater = Updater(token=cfg.TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Help info")

def show_list(update, context):
	f = open('result.png', 'rb')


	with open('images/hm.jpg', 'rb') as f1, open('result.png', 'rb') as f2:
		context.bot.send_media_group(chat_id=update.effective_chat.id,
			media=[InputMediaPhoto(f1), InputMediaPhoto(f2)])

def msgCallback(update, context):
	args = update.message.text.split()
	if len(args) < 2:
		context.bot.send_message(chat_id=update.effective_chat.id, 
			text='Писать надо так:\n\t<номер картинки> <текст>')

	txt = update.message.text.replace(args[0], '')

	if len(txt) > 150:
		return context.bot.send_message(chat_id=update.effective_chat.id, 
			text='Текст должен быть короче 150 символов')

	try:
		img = cfg.IMAGES[args[0]]
		photo = utils.generate_image(img, txt)

		return context.bot.send_photo(chat_id=update.effective_chat.id,
			photo=photo)
	except KeyError:
		return context.bot.send_message(chat_id=update.effective_chat.id, 
			text='Нет картинки "%s"' % args[0])


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

list_handler = CommandHandler('list', show_list)
dispatcher.add_handler(list_handler)

msg_handler = MessageHandler(Filters.text, msgCallback)
dispatcher.add_handler(msg_handler)

updater.start_polling()
updater.idle()