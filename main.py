from extension import CryptoConversion, ConversionException
from config import keys, token
import telebot


bot = telebot.TeleBot(token)


@bot.message_handler(['help', 'start'])
def help(message:telebot.types.Message):
    text = 'Этот бот поможет узнать количество валюты которое вы получите после обмен. Чтобы узнать допустимые валюты /values'
    bot.reply_to(message, text)

@bot.message_handler(['values', ])
def values (message:telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        keys1 = (f'{key} : {keys[key]}')
        text = '\n'.join((text, keys1))
    text = '\n'.join((text, 'Чтобы узнать курс обмена используйте след макет', '\n', 'валюта валюта количество', 'USD EUR 2000'))

    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert (message:telebot.types.Message):
    try:
        value = message.text.split(' ')
        if len(value) != 3:
            raise ConversionException('Слишком много или мало параметров')
        base, quote, amount = value
        total_base = CryptoConversion.convert(quote, base, amount)
    except ConversionException as e:
        bot.reply_to(message, f'Ошибка пользователя > /help \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка в коде > /help \n{e}')
    else:
        text = (f'За {amount} {base} вы получите {total_base*float(amount)} {quote}') #*float(amount)
        print(type(total_base))
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)