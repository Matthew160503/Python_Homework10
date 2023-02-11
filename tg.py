import telebot
from telebot import types
import time

bot = telebot.TeleBot('6078445605:AAFGcq-zH8_HTqgFtjBNrpJzOeK6WvqjVd0')

value = ''
old_value = ''
c_list = []
res = 0

markup = types.InlineKeyboardMarkup()
key1 = types.InlineKeyboardButton('Выход', callback_data = 'Выход')
key2 = types.InlineKeyboardButton('C', callback_data = 'C')
key3 = types.InlineKeyboardButton('<=', callback_data = '<=')
key4 = types.InlineKeyboardButton('=', callback_data = '=')

key5 = types.InlineKeyboardButton('7', callback_data = '7')
key6 = types.InlineKeyboardButton('8', callback_data = '8')
key7 = types.InlineKeyboardButton('9', callback_data = '9')
key8 = types.InlineKeyboardButton('*', callback_data = '*')

key9 = types.InlineKeyboardButton('4', callback_data = '4')
key10 = types.InlineKeyboardButton('5', callback_data = '5')
key11 = types.InlineKeyboardButton('6', callback_data = '6')
key12 = types.InlineKeyboardButton('/', callback_data = '/')

key13 = types.InlineKeyboardButton('0', callback_data = '0')
key14 = types.InlineKeyboardButton('1', callback_data = '1')
key15 = types.InlineKeyboardButton('2', callback_data = '2')
key16 = types.InlineKeyboardButton('3', callback_data = '3')

key17 = types.InlineKeyboardButton('-', callback_data = '-')
key18 = types.InlineKeyboardButton('+', callback_data = '+')
key19 = types.InlineKeyboardButton('%', callback_data = '%')
key20 = types.InlineKeyboardButton('.', callback_data = '.')
markup.row(key1, key2, key3, key4)
markup.row(key5, key6, key7, key8)
markup.row(key9, key10, key11, key12)
markup.row(key13, key14, key15, key16)
markup.row(key17, key18, key19, key20)

@bot.message_handler(commands=['start'])
def start(message):
    path = open('text.txt','a',encoding='utf-8')
    path.write(f'First name: {message.from_user.first_name},id: {message.from_user.id}, current time: {time.asctime()} \n')
    keyboard = types.ReplyKeyboardMarkup()
    path.close()
    k1 = types.KeyboardButton('Рациональные')
    k2 = types.KeyboardButton('Комплексные')
    keyboard.add(k1,k2)
    bot.send_message(message.chat.id, f'{message.from_user.first_name}, Добро пожаловать в калькулятор для подсчета'+
    ' рациональных и комплексных чисел! Для дальнейшего подсчета выберите категорию чисел ниже', reply_markup= keyboard)
    bot.register_next_step_handler(message, category_definition)

def category_definition(message):
    if message.text == 'Рациональные':
        bot.send_message(message.chat.id, 'Выберите команду /rational_calculator')
    elif message.text == 'Комплексные':
        bot.send_message(message.chat.id, 'Выберите команду /complex_calculator')

@bot.message_handler(commands = ['rational_calculator'])
def rational_number(message):
    global value
    if value == '':
        bot.send_message(message.from_user.id, '0', reply_markup = markup)
    else:
        bot.send_message(message.from_user.id, value, reply_markup = markup)

@bot.callback_query_handler(func=lambda call:True)
def callback_func(query):
    global value, old_value
    data = query.data
    if data == 'C':
        value = ''
    elif data ==    '<=':
        value = value[:len(value)-1]
    elif data == 'Выход':
        value = 'Выход из калькулятора выполнен.'
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value, reply_markup = markup)
    elif data == '=':
        try:
            value = str(eval(value))
        except:
            value = 'Ошибка!'
    else:
        value += data
    if value == 'Выход из калькулятора выполнен.':
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='Если Вы желаете использовать калькулятор снова нажмите /start. А для выхода из программы нажмите /exit', reply_markup = markup)
        value = ''
    else:
        if (value != old_value and value !='') or ('0' != old_value and value == ''):
            if value == '':
                bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='0', reply_markup = markup)
                old_value = '0'
            else:
                bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text = value, reply_markup = markup)
                old_value = value
        if value == 'Ошибка!': value = ''

@bot.message_handler(commands = ['complex_calculator'])
def complex_calculator(message):
    bot.send_message(message.chat.id, 'Введите два комплексных числа через пробел')
    bot.register_next_step_handler(message, complex_calculate)

def complex_calculate(message):
    global c_list
    c_list = list(map(complex,message.text.split()))
    bot.send_message(message.chat.id, f'введите знак операции (+,-,/,*): ')
    bot.register_next_step_handler(message, result)

def result(message):
    global c_list, res
    if message.text == '+':
        for i in c_list:
            res += i
        bot.send_message(message.from_user.id, f'Результат суммы равен {res}')
    elif message.text == '-':
        res = c_list[0]-c_list[1]
        bot.send_message(message.from_user.id, f'Результат разности равен {res}')
    elif message.text == '*':
        res = c_list[0] * c_list[1]
        bot.send_message(message.from_user.id, f'Результат произведения равен {res}')
    elif message.text == '/':
        res = c_list[0] / c_list[1]
        bot.send_message(message.from_user.id, f'Результат деления равен {res}')
    else:
        bot.send_message(message.chat.id, 'Такой операции для комплексных чисел нет')
    c_list.clear()
    res = 0
    bot.send_message(message.chat.id, f'Если Вы желаете использовать калькулятор комплексных числе снова нажмите /complex_calculator. Для выбора категироии калькулятора - /start, a для выхода из программы - /exit')


@bot.message_handler(commands=['exit'])
def exit(message):
    if message == '/exit':
        bot.stop_polling()

bot.polling()