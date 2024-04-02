import telebot
import requests
import time

# Токен вашего бота в Telegram
TOKEN = '7155706644:AAFfDhhP9X0BdhGDoXjrxfP5GsJZG-9ilIk'

# Создание экземпляра бота
bot = telebot.TeleBot(TOKEN)


# Функция для получения текущего курса доллара
def get_usd_rate():
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    data = response.json()
    usd_rate = data['Valute']['USD']['Value']
    return usd_rate


# Глобальные переменные для хранения границ курса доллара
upper_bound = None
lower_bound = None

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, "Привет, чтобы начать работу со мной, напиши команду /setbounds")


# Обработчик команды /setbounds для установки границ курса доллара
@bot.message_handler(commands=['setbounds'])
def set_bounds(message):
    global upper_bound, lower_bound
    chat_id = message.chat.id
    if upper_bound is None:
        bot.send_message(chat_id, 'Введите верхнюю границу курса доллара:')
        bot.register_next_step_handler(message, set_upper_bound)
    else:
        bot.send_message(chat_id, f'Текущие границы курса доллара: Верхняя - {upper_bound}, Нижняя - {lower_bound}.'
                                   '\nХотите изменить границы? (да/нет)')
        bot.register_next_step_handler(message, confirm_change_bounds)



def confirm_change_bounds(message):
    global upper_bound, lower_bound
    chat_id = message.chat.id
    user_response = message.text.lower()
    if user_response == 'да':
        upper_bound = None
        lower_bound = None
        bot.send_message(chat_id, 'Введите новую верхнюю границу курса доллара:')
        bot.register_next_step_handler(message, set_upper_bound)
    elif user_response == 'нет':
        bot.send_message(chat_id, 'Операция отменена.')
    else:
        bot.send_message(chat_id, 'Пожалуйста, введите "да" или "нет".')



def set_upper_bound(message):
    global upper_bound
    chat_id = message.chat.id
    upper_bound = float(message.text)
    bot.send_message(chat_id, 'Введите нижнюю границу курса доллара:')
    bot.register_next_step_handler(message, set_lower_bound)


def set_lower_bound(message):
    global lower_bound
    chat_id = message.chat.id
    lower_bound = float(message.text)

    while True:
        usd_rate = get_usd_rate()
        if usd_rate > upper_bound or usd_rate < lower_bound:
            bot.send_message(chat_id, f'Курс доллара вышел за заданные границы: {usd_rate}')
        else:
            bot.send_message(chat_id, f'Курс доллара в норме: {usd_rate}')
        time.sleep(60)  # Проверяем курс раз в минуту


# Запуск бота
bot.polling(none_stop=True)
