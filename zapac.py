import telebot
from telebot import types
from random import choice
import sqlite3

bot = telebot.TeleBot("5205222942:AAFEtwRwlk7WRWA2AcWA0ubP0XqD277qIu0")

termin = {"медиана": "― отрезок, соединяющий вершину треугольника с серединой противоположной стороны.",
          "биссектриса": "— луч, исходящий из вершины угла и делящий этот угол на два равных угла.",
          "высота": "— отрезок перпендикуляра, опущенного из вершины геометрической фигуры (например, треугольника, "
                    "пирамиды, конуса) на её основание или на продолжение основания. ",
          "чевиана":
              "— это отрезок в треугольнике, соединяющий вершину треугольника с точкой на противоположной стороне."}

video = {
    "тригонометрия": ["https://youtu.be/Z5PrN6xen1g", "https://youtu.be/vlcWmtk_auI", "https://youtu.be/pIZgr_dNyqQ"],
    "логарифмы": ["https://youtu.be/iGLQTAsWZ3Q", "https://youtu.be/oZX73ykRzno", "https://youtu.be/_65tfvYrAko"],
    "параметры": ["https://youtu.be/xNszdUaem44", "https://youtu.be/_Fn0d4gScDE", "https://youtu.be/A7wSwLENces"],
    "геометрия": ["https://youtu.be/JMT31jRvFt0", "https://youtu.be/D-TpAn4dV6c", "https://youtu.be/aHqa-cLd8d4"],
    "разборы вариантов егэ": ["https://youtu.be/oR-j2oGwKWY", "https://youtu.be/rHb93bH0o08",
                              "https://youtu.be/BaY2hNjH_Jk"], "разборы вариантов огэ":
        ["https://youtu.be/5wrzTnLWiNM", "https://youtu.be/DbOYpP7djmY", "https://youtu.be/v1n1ygezg44"]}
# видео по темам и ссылки на них

vthemes = ["Тригонометрия", "Логарифмы", "Параметры", "Геометрия", "Разборы вариантов ОГЭ", "Разборы вариантов ОГЭ"]

formulass = {"объём шара": "Vshara.jpg", "площадь шара": "Sshara.png", "объём конуса": "Vkonus.jpg"}

meme = ['1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg']

task = [["Книга содержит N страниц, которые пронумерованы стандартно: от 1 до N. Если сложить количество цифр (не "
         "сами числа), что содержатся в каждом номере страницы, выйдет 1095. Так сколько в книге страниц?", "401"],
        ["Попробуйте в уме разделить 30 на 1/2 и прибавить 10. Каким будет результат?", "70"],
        ["Сколько целых чисел в диапазоне 1-1000 вмещают в себя цифру 3?", "271"],
        ["Вес дыни равен суммарному весу арбуза и лимона. Вес дыни и лимона вместе равен суммарному весу двух "
         "арбузов. Сколько потребуется лимонов, чтобы выровнять весы, на которых лежит дыня?", "3 лимона"]]


@bot.message_handler(commands=['start'])
def start(message):  # это функция для вывода "приветственного сообщения"
    m = f'Привет, <b>{message.from_user.first_name} <u>{message.from_user.last_name}</u></b>!'
    m2 = f'Напиши <b><u>{"/info"}</u></b> для того, чтобы узнать, какие у меня есть команды!'
    bot.send_message(message.chat.id, f'{m}\n{m2}', parse_mode='html')


@bot.message_handler(commands=['info'])
def info(message):
    m = "Вот список известных мне команд:"
    m1 = f'<b><u>/start</u></b> - начало работы бота, вывод приветственного сообщения'
    m2 = f'<b><u>/info</u></b> - список команд бота'
    m3 = f'<b><u>/termins</u></b> - помощь с определениями математических терминов'
    m4 = f'<b><u>/videos</u></b> - подборка видеоуроков по математике на заданную тему'
    m5 = f'<b><u>/formulas</u></b> - помощь с формулами по геометрии и алгебре'
    m6 = f'<b><u>/number</u></b> - расскажу о делителях числа'
    m7 = f'<b><u>/memes</u></b> - отправлю мем про учёбу'
    m8 = f'<b><u>/tasks</u></b> - задам задачку на логику'
    bot.send_message(message.chat.id, f'<b><u>{m}</u></b>\n{m1}\n{m2}\n{m3}\n{m4}\n{m5}\n{m6}\n{m7}\n{m8}',
                     parse_mode='html')


@bot.message_handler(commands=['videos'])
def videos(message):  # вывод списка тем, на которые есть видео
    if message.text == '/videos':
        m = "Вот темы, на которые у меня есть видеоподборки:"
        m2 = "Напиши название темы, которая тебя интересует."
        v = "\n".join(vthemes)
        bot.send_message(message.chat.id, f'<u><b>{m}</b></u>\n{v}\n<b> {m2}</b>', parse_mode='html')
        bot.register_next_step_handler(message, get_videos)


def get_videos(message):  # вывод ссылок на видеоуроки
    con = sqlite3.connect("math_bd.db")
    cur = con.cursor()
    theme = cur.execute("""SELECT theme FROM videos""").fetchall()
    them = []
    for j in theme:
        them.append(j[0])
    if message.text.lower() in them:
        result2 = cur.execute("""SELECT link1,link2,link3 FROM videos
                                 WHERE theme = ?""", (message.text.lower(),)).fetchall()
        f = []
        for k in result2[0]:
            f.append(k)
        answer = "\n".join(f)
        bot.send_message(message.chat.id, f'<b>Вот видеоуроки по теме, которая тебя заинтересовала:</b>\n {answer}',
                         parse_mode='html')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
                         text="Хочешь ещё одну подборку видеоуроков?".format(
                             message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, yes_no_videos)
    else:
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)  # если пользователь ввёл не тему из списка предложенных
        button1 = types.KeyboardButton("Выбрать другую тему")  # он может заново ввести название темы, либо воспользоваться другими командами
        button2 = types.KeyboardButton("Другие функции")
        markup2.add(button1, button2)
        bot.send_message(message.chat.id, "У меня нет видеоуроков на эту тему, выбери одну из списка или воспользуйся "
                                          "другими моими функциями!", reply_markup=markup2)
        bot.register_next_step_handler(message, videos_or_no)


def yes_no_videos(message):  # выбор пользователя при корректном вводе темы
    if message.text == "Да":
        bot.send_message(message.chat.id, text="Выбери тему из списка!", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_videos)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, text="Можешь воспользоваться другими моими функциями!",
                         reply_markup=types.ReplyKeyboardRemove())


def videos_or_no(message):  # выбор пользователя при некорректном вводе темы
    if message.text == "Выбрать другую тему":
        m1 = f'<b><u>{"Выбери тему из списка!"}</u></b>'
        m2 = "\n".join(vthemes)
        bot.send_message(message.chat.id, text=f'{m1}\n{m2}',
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_videos)
    elif message.text == "Другие функции":
        bot.send_message(message.chat.id,
                         text=f'Напиши <b><u>{"/info"}</u></b> для того, чтобы узнать, какие у меня есть команды!',
                         parse_mode='html', reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['termins'])
def termins(message):
    if message.text == '/termins':  # описание работы команды /termins
        m = "Напиши термин, определение которого ты хочешь узнать!"
        m1 = "Укажи его в именительном падеже"
        bot.send_message(message.chat.id, f'{m}\n{m1}', parse_mode='html')
        bot.register_next_step_handler(message, get_termins)


def get_termins(message):  # обработка сообщения пользователя и вывод определения интересующего его термина
    con = sqlite3.connect("math_bd.db")
    cur = con.cursor()
    res = cur.execute("""SELECT termin FROM termins""").fetchall()
    termins = []
    for j in res:
        termins.append(j[0])
    if message.text.lower() in termins:
        result2 = cur.execute("""SELECT info FROM termins
                                 WHERE termin = ?""", (message.text,)).fetchall()
        bot.send_message(message.chat.id, result2[0][0], parse_mode='html')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
                         text="Хочешь узнать определение ещё одного термина?".format(
                             message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, yes_no_termins)
    else:
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Ввести другой термин")
        button2 = types.KeyboardButton("Другие функции")
        markup2.add(button1, button2)
        bot.send_message(message.chat.id, "Мне неизвестен этот термин, попробуй ввести другой или воспользоваться "
                                          "остальными моими функциями!", reply_markup=markup2)
        bot.register_next_step_handler(message, termins_or_no)


def yes_no_termins(message):
    if message.text == "Да":
        bot.send_message(message.chat.id, text="Выбери тему из списка!", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_termins)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, text="Можешь воспользоваться другими моими функциями!",
                         reply_markup=types.ReplyKeyboardRemove())


def termins_or_no(message):
    if message.text == "Ввести другой термин":
        bot.send_message(message.chat.id, text='Напиши термин, который тебя интересует в именительном падеже!',
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_termins)
    elif message.text == "Другие функции":
        bot.send_message(message.chat.id,
                         text=f'Напиши <b><u>{"/info"}</u></b> для того, чтобы узнать, какие у меня есть команды!',
                         parse_mode='html', reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['formulas'])
def formulas(message):
    m1 = "Какую формулу ты хочешь узнать?"
    m2 = "Напиши название в именительном падеже!"
    bot.send_message(message.chat.id, f'{m1}\n{m2}')
    bot.register_next_step_handler(message, get_formulas)


def get_formulas(message):
    if message.text.lower() in formulass.keys():  # формулы
        name = formulass.get(message.text.lower())
        formula = open(name, 'rb')
        bot.send_photo(message.chat.id, formula)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
                         text="Хочешь узнать еще какие-то формулы?".format(
                             message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, yes_no_termins)
    else:
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Ввести другую формулу")
        button2 = types.KeyboardButton("Другие функции")
        markup2.add(button1, button2)
        bot.send_message(message.chat.id, "Мне неизвестна эта формула, попробуй ввести название другой или "
                                          "воспользоваться остальными моими функциями!", reply_markup=markup2)
        bot.register_next_step_handler(message, formulas_or_no)


def yes_no_formulas(message):
    if message.text == "Да":
        bot.send_message(message.chat.id,
                         text=f'Какую формулу ты хочешь узнать?\nНапиши название в именительном падеже!',
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_formulas)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, text="Можешь воспользоваться другими моими функциями!",
                         reply_markup=types.ReplyKeyboardRemove())


def formulas_or_no(message):
    if message.text == "Ввести другую формулу":
        bot.send_message(message.chat.id, text='Напиши название формулы, которую ты хочешь узнать в именительном '
                                               'падеже!', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_formulas)
    elif message.text == "Другие функции":
        bot.send_message(message.chat.id,
                         text=f'Напиши <b><u>{"/info"}</u></b> для того, чтобы узнать, какие у меня есть команды!',
                         parse_mode='html', reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['number'])
def number(message):  # Расскажет о четности, о простАте, мин и макс делитель и колво делителей
    m1 = "Введи натуральное число и я выдам тебе информацию о нём:"
    m2 = "Чётность, простота, наименьший и наибольший делители, количество делителей"
    bot.send_message(message.chat.id, f'<b><u>{m1}</u></b>\n{m2}', parse_mode='html')
    bot.register_next_step_handler(message, get_number)


def get_number(message):
    if message.text.isnumeric() == True:
        num = int(message.text)
        deliteli = []
        chet = ''
        prost = ''
        for i in range(1, int(num ** 0.5) + 1):
            if i * i == num:
                deliteli.append(i)
            elif num % i == 0:
                deliteli.append(i)
                deliteli.append(num // i)
        deliteli.sort()
        if num % 2 == 0:
            chet = 'чётное'
        else:
            chet = 'нечётное'
        if len(deliteli) == 2:
            prost = 'простое'
        else:
            prost = 'составное'
        bot.send_message(message.chat.id, f'Это число - {chet}, {prost}.\nУ него {str(len(deliteli))} делителей.\n'
                                          f'Наибольший делитель числа, отличный от него самого - {deliteli[-1]}.\n'
                                          f'Наименьший делитель числа, отличный от единицы - {deliteli[1]}.',
                         parse_mode='html')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
                         text="Хочешь узнать информацию о других числах?".format(
                             message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, yes_no_number)
    else:
        markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Ввести другое число")
        button2 = types.KeyboardButton("Другие функции")
        markup2.add(button1, button2)
        bot.send_message(message.chat.id, "Введи натуральное число без дополнительных символов или "
                                          "воспользуйся другими моими функциями!", reply_markup=markup2)
        bot.register_next_step_handler(message, numbers_or_no)


def yes_no_number(message):
    if message.text == "Да":
        bot.send_message(message.chat.id, text="Напиши новое интересующее тебе число",
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_number)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, text="Можешь воспользоваться другими моими функциями!",
                         reply_markup=types.ReplyKeyboardRemove())


def numbers_or_no(message):
    if message.text == "Ввести другое число":
        bot.send_message(message.chat.id, text='Введи натуральное число без дополнительных символов и я выдам тебе '
                                               'информацию о нём!', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_number)
    elif message.text == "Другие функции":
        bot.send_message(message.chat.id,
                         text=f'Напиши <b><u>{"/info"}</u></b> для того, чтобы узнать, какие у меня есть команды!',
                         parse_mode='html', reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['memes'])
def memes(message):
    if message.text == "/memes":
        bot.send_message(message.chat.id, "Вот тебе мем для поднятия настроения!:)")
        name = choice(meme)
        pic = open(name, 'rb')
        bot.send_photo(message.chat.id, pic)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Да")
        btn2 = types.KeyboardButton("Нет")
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id,
                         text="Хочешь ещё один мем?".format(
                             message.from_user), reply_markup=markup)
        bot.register_next_step_handler(message, yes_no_memes)

def yes_no_memes(message):
    if message.text == "Да":
        bot.send_message(message.chat.id, f'Напиши <b><u>{"/memes"}</u></b> ещё разок!', parse_mode='html',
                         reply_markup=types.ReplyKeyboardRemove())
    elif message.text == "Нет":
        bot.send_message(message.chat.id, text="Можешь воспользоваться другими моими функциями!",
                         reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['tasks'])
def tasks(message):
    if message.text == "/tasks":
        bot.send_message(message.chat.id, f'<b>Вот тебе задачка на логику!</b>', parse_mode='html')
        global t
        t = choice(task)
        bot.send_message(message.chat.id, t[0])
        bot.register_next_step_handler(message, right_or_no)


def right_or_no(message):
    if message.text == t[1]:
        bot.send_message(message.chat.id, f'Ты ответил верно, молодец!', parse_mode='html')
    else:
        bot.send_message(message.chat.id, f'Верный ответ - <b><u>{t[1]}</u></b>', parse_mode='html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Да")
    btn2 = types.KeyboardButton("Нет")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id,
                     text="Хочешь ещё одну задачку?".format(
                         message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, yes_no_tasks)


def yes_no_tasks(message):
    if message.text == "Да":
        bot.send_message(message.chat.id, f'Напиши <b><u>{"/tasks"}</u></b> ещё разок!', parse_mode='html',
                         reply_markup=types.ReplyKeyboardRemove())
    elif message.text == "Нет":
        bot.send_message(message.chat.id, text="Можешь воспользоваться другими моими функциями!",
                         reply_markup=types.ReplyKeyboardRemove())


bot.polling(none_stop=True)
