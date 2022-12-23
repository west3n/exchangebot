import telebot
from token_keys import TOKEN, keys
from extentions import ConversionException, Converter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Добро пожаловать в ExchangeBot! Чтобы понять, как работает бот, жмите на /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Этот бот предназначен для конвертации разных валют. \nДля того, чтообы узнать список валют, жмите на /values. \nЧтобы сравнить 2 валюты, вам необходимо ввести запрос в таком формате: \n<1ая валюта> <2ая валюта> <Количество>, например: \nДоллар Рубль 200'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['audio', 'photo', 'document', 'voice', 'sticker', 'video', 'location', 'animation'])
def error(message: telebot.types.Message):
    text = 'Очень любопытно, но бот работает только с текстом'
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise ConversionException("Неверные параметры. Используйте рекомендуемый шаблон.\n<1ая валюта> <2ая валюта> <Количество>")

        quote, base, amount = values
        total_base = Converter.convert(str(quote).lower(), str(base).lower(), amount)
    except ConversionException as e:
        bot.reply_to(message, f'{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Результат конвертации - {total_base * float(amount)}'
        bot.send_message(message.chat.id, text)


bot.polling()
