from keys import telegram_token_secret as my_secret
import feedparser
import json

from telegram.ext import CallbackContext
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)

# Включим ведение журнала
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Определяем константы этапов разговора
GENDER, PHOTO, LOCATION, BIO = range(4)

reply_keyboard = [['Да', 'Нет']]

# функция обратного вызова точки входа в разговор
#
#def serials(update, _):
#    # Список кнопок для ответа
#    reply_keyboard = [["БАН", "НЕ БАН"]]
#    # Создаем простую клавиатуру для ответа
#    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
#    # Начинаем разговор с вопроса
#    feed_data = feedparser.parse("http://seasonvar.ru/rss.php")
##    z = json.loads(feed_data["entries"][0]["title"])
#    z = feed_data["entries"][0]["title"]
#    x = feed_data["entries"][0]["link"]
#    update.message.reply_text(
#        f'Название - {z} ',
#        f'Ссылка - {x} ',
#        reply_markup=markup_key,)
    # переходим к этапу `GENDER`, это значит, что ответ
    # отправленного сообщения в виде кнопок будет список 
    # обработчиков, определенных в виде значения ключа `GENDER`
    
#    for z in feed_data["entries"]:
#        if "сезон полностью" in z["title"].split(" серия")[0].split(",")[-1].lstrip():
#            ep = "сезон полностью"
#            title=z["title"].split(",")[0].split("(")[0].rstrip(),
#            img=z["link"].split("-")[1],
#            serial_and_season="".join(z["title"].split(",")[:-1]),
#            episode=ep,
#        else:
#            ep = z["title"].split(" серия")[0].split(",")[-1].lstrip()
#            title=z["title"].split(",")[0].split("(")[0].rstrip(),
#            img =  z["link"].split("-")[1],
#            serial_and_season = "".join(z["title"].split(",")[:-1]),
#            episode = ep,
#    context.bot.send_message(chat_id=update.effective_chat.id, text=x)

#    return GENDER
    
#при команде /start в чате выйдет сообщение из text=""
#def start(update: Update, context: CallbackContext):
#    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
def get_serials(update, _):
    feed_data = feedparser.parse("http://seasonvar.ru/rss.php")
#    z = json.loads(feed_data["entries"][0]["title"])
#    title = feed_data["entries"][0]["title"]
    link = feed_data["entries"][0]["link"]
#    update.message.reply_text(
#        f'Название - {z} ',
#        f'Ссылка - {x} ',
#        reply_markup=markup_key,)
    # переходим к этапу `GENDER`, это значит, что ответ
    # Список кнопок для ответа
#    reply_keyboard = [['Да', 'Нет']]
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # Начинаем разговор с вопроса
    update.message.reply_text(
        f'{link} Отслеживать этот сериал? \n\n',
        reply_markup=markup_key,)
    # переходим к этапу `GENDER`, это значит, что ответ
    # отправленного сообщения в виде кнопок будет список 
    # обработчиков, определенных в виде значения ключа `GENDER`
    return GENDER

# Обрабатываем пол пользователя
def ban_or_no(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Здесь будет ставиться маркер БД - банить этот сериал или нет, а пока вывожу в логи
    logger.info(
            'Ставлю метку в БД на вопрос выбор'
            f'отслеживать - не отслеживать {update.message.text}'
    )
    # Создаем простую клавиатуру для ответа
    markup_key = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    # Уточняем хочет ли пользователь добавить ссылку для отслеживаниня сериала
    update.message.reply_text(
        f'Хотите ли вы сделать заметку или ввести альтернативный '
        'источик для просмотра этого сериала? \n\n',
        reply_markup=markup_key,)

    # Следующее сообщение с удалением клавиатуры `ReplyKeyboardRemove`
#    reply_markup=ReplyKeyboardRemove(),
    # переходим к этапу `PHOTO`
    return PHOTO

# Получаем заметку от пользователя
def get_user_note(update, _):
    # определяем пользователя
    user = update.message.from_user
    # получаем заметку или ссылку от пользователя
    note_or_link = update.message
#    photo_file = .photo[-1].get_file()
    # скачиваем фото 
#    photo_file.download(f'{user.first_name}_photo.jpg')
    # Пишем в журнал сведения о фото
#    logger.info("Фотография %s: %s", user.first_name, f'{user.first_name}_photo.jpg')
    logger.info("Заметка или ссылка от пользователя %s: %s", user.first_name, f'{note_or_link}')
    # Отвечаем на сообщение с фото
    update.message.reply_text(
            'Заметка или ссылка сохранена в базу'
    )
    # переходим к этапу `LOCATION`
    return LOCATION

# Обрабатываем команду /skip для фото
def ban(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал сведения о фото
    logger.info("Пользователь %s не желает отслеживать этот сериал", user.first_name)
    # Отвечаем на сообщение с пропущенной фотографией
    update.message.reply_text(
            'Нужно продумать, как пользователю вбить заметку, '
            'если он захочет её вбить позже.\n\n'
    )
    # переходим к этапу `LOCATION`
    return LOCATION

# Обрабатываем местоположение пользователя
def location(update, _):
    # определяем пользователя
    user = update.message.from_user
    # захватываем местоположение пользователя
    user_location = update.message.location
    # Пишем в журнал сведения о местоположении
    logger.info(
        "Местоположение %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude)
    # Отвечаем на сообщение с местоположением
    update.message.reply_text(
        'Может быть, я смогу как-нибудь навестить тебя!' 
        ' Расскажи мне что-нибудь о себе...'
    )
    # переходим к этапу `BIO`
    return BIO

# Обрабатываем команду /skip для местоположения
def skip_location(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал сведения о местоположении
    logger.info("User %s did not send a location.", user.first_name)
    # Отвечаем на сообщение с пропущенным местоположением
    update.message.reply_text(
        'Точно параноик! Ну ладно, тогда расскажи мне что-нибудь о себе...'
    )
    # переходим к этапу `BIO`
    return BIO

# Обрабатываем сообщение с рассказом/биографией пользователя
def bio(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал биографию или рассказ пользователя
    logger.info("Пользователь %s рассказал: %s", user.first_name, update.message.text)
    # Отвечаем на то что пользователь рассказал.
    update.message.reply_text('Спасибо! Надеюсь, когда-нибудь снова сможем поговорить.')
    # Заканчиваем разговор.
    return ConversationHandler.END

# Обрабатываем команду /cancel если пользователь отменил разговор
def cancel(update, _):
    # определяем пользователя
    user = update.message.from_user
    # Пишем в журнал о том, что пользователь не разговорчивый
    logger.info("Пользователь %s отменил разговор.", user.first_name)
    # Отвечаем на отказ поговорить
    update.message.reply_text(
        'Мое дело предложить - Ваше отказаться'
        ' Будет скучно - пиши.', 
        reply_markup=ReplyKeyboardRemove()
    )
    # Заканчиваем разговор.
    return ConversationHandler.END
#
#
#def cancel(update, _):
#    # определяем пользователя
#    user = update.message.from_user
#    # Пишем в журнал о том, что пользователь не разговорчивый
#    logger.info("Пользователь %s отменил разговор.", user.first_name)
#    # Отвечаем на отказ поговорить
#    update.message.reply_text(
#        'Мое дело предложить - Ваше отказаться'
#        ' Будет скучно - пиши.', 
#        reply_markup=ReplyKeyboardRemove()
#    )
#    # Заканчиваем разговор.
#    return ConversationHandler.END
#
##функция echo повторяет сообщения
#def echo(update: Update, context: CallbackContext):
#    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
#
## При написание команды /caps последующие символы выйдут в верхнем регистре
#def caps(update: Update, context: CallbackContext):
#    text_caps = ' '.join(context.args).upper()
#    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
#
#
#def inline_caps(update: Update, context: CallbackContext):
#    query = update.inline_query.query
#    if not query:
#        return
#    results = []
#    results.append(
#        InlineQueryResultArticle(
#            id=query.upper(),
#            title='Caps',
#            input_message_content=InputTextMessageContent(query.upper())
#        )
#    )
#    context.bot.answer_inline_query(update.inline_query.id, results)
#
##При команде через / если команда неизвеста, выйдет сообщение
#def unknown(update: Update, context: CallbackContext):
#    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
#
#
#conv_handler = ConversationHandler(
#        entry_points=[CommandHandler('serials', serials)],
#        states={
#            GENDER: [MessageHandler(Filters.regex('^(БАН|НЕ БАН)$'), serials)],
#            },
#        fallbacks=[CommandHandler('cancel', cancel)],
#        )
#
## Добавляем обработчик разговоров `conv_handler`
#dispatcher.add_handler(conv_handler)
#
#inline_caps_handler = InlineQueryHandler(inline_caps)
#dispatcher.add_handler(inline_caps_handler)
#
#caps_handler = CommandHandler('caps', caps)
#dispatcher.add_handler(caps_handler)
#
#echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
#dispatcher.add_handler(echo_handler)
#
##start_handler = CommandHandler('start', start)
##dispatcher.add_handler(start_handler)
#
#serials_handler = CommandHandler('serials', serials)
#dispatcher.add_handler(serials_handler)
#
#unknown_handler = MessageHandler(Filters.command, unknown)
#dispatcher.add_handler(unknown_handler)
#
#updater.start_polling()

if __name__ == '__main__':
    # Создаем Updater и передаем ему токен вашего бота.
    updater = Updater(my_secret)
    # получаем диспетчера для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Определяем обработчик разговоров `ConversationHandler` 
    # с состояниями GENDER, PHOTO, LOCATION и BIO
    conv_handler = ConversationHandler( # здесь строится логика разговора
        # точка входа в разговор
        entry_points=[CommandHandler('go', get_serials)],
        # этапы разговора, каждый со своим списком обработчиков сообщений
        states={
            GENDER: [MessageHandler(Filters.regex('^(Да|Нет)$'), get_serials)],
            PHOTO: [MessageHandler(Filters.regex('^(Да|Нет)$'), ban_or_no), CommandHandler('skip', ban)],
            LOCATION: [
                MessageHandler(Filters.location, location),
                CommandHandler('skip', get_user_note),
            ],
            BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        # точка выхода из разговора
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Добавляем обработчик разговоров `conv_handler`
    dispatcher.add_handler(conv_handler)

    # Запуск бота
    updater.start_polling()
    updater.idle()
