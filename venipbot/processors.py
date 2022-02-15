"""
ТУТ ТОЛЬКО ЯРОСТНОЕ БЕЗКОМПРОМИСНОЕ ЛЕГАСИ
ЕСЛИ ЧИТАЕШ ЭТО !!!!БЕГИ!!!!
(c) тот кто это все кодил

cd /var/www/mysite
python3 manage.py runserver

sh start.sh
fuser -k 8000/tcp

git config --global user.name "Name" 
git config --global user.email "email@mail.ru"

"""
# InlineKeyboardButton.a('Ссылочная кнопка', url='https://google.com'),
from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.inlinekeyboardbutton import InlineKeyboardButton
from django_tgbot.types.inlinekeyboardmarkup import InlineKeyboardMarkup
from django_tgbot.types.keyboardbutton import KeyboardButton
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.update import Update
from .bot import state_manager
from .models import TelegramState
from .bot import TelegramBot
from MarketBot.models import Категория, Подкатегория, Продукт, UseCategory, basket, Акции, addresses, orders, buket_arhiv
import datetime, requests
from django.db.models import Q
import uuid
from yookassa import Configuration, Payment
from django.conf import settings



state_manager.set_default_update_types(update_types.Message)



# обработчик отправленных пользователем сообщений(кнопок меню)
@processor(state_manager, from_states=state_types.Reset, message_types=[message_types.Text])
def send_keyboards(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    text = str(update.get_message().get_text())
    # bot.sendMessage(chat_id, text='Пока работает', parse_mode=bot.PARSE_MODE_MARKDOWN)

    # создание переменной globall если её нет
    if UseCategory.objects.filter(chatid=chat_id).exists():
        globall = UseCategory.objects.filter(chatid=chat_id)
        globall = int(globall[0].globall)
    else:
        globall=0
    # создание переменной globall если её нет
    
    if text in ['В начало', '/start']:
        handler0(chat_id)
        send_start_keyboard(bot, chat_id)
    # elif text in ['Gulad']:
    #     send_start_keyboard(bot, chat_id)
    #     Gulad()
    #     send_start_keyboard(bot, chat_id)
    elif text in ['Личный кабинет']:
        handler0(chat_id)
        send_lk_keyboard(bot, chat_id)
    elif 'Корзина' in text:
        handler0(chat_id)
        send_basket_keyboard(bot, chat_id)
    elif text in ['Отмена']:
        handler0(chat_id)
        send_basket_keyboard(bot, chat_id)
    elif text in ['Акции']:
        handler0(chat_id)
        action(bot, chat_id, 0)
    elif text in ['Оператор']:
        handler0(chat_id)
        send_start_keyboard(bot, chat_id)
    elif text in ['Выбрать товар']:
        handler0(chat_id)
        send_tovar_keyboard(bot, chat_id)

    if UseCategory.objects.filter(chatid=chat_id).exists():
        handler = UseCategory.objects.filter(chatid=chat_id)
        if handler[0].handler == None:
            handler0(chat_id)

    
        if handler[0].handler == "0":
            if 'Оплатить' in text:
                message_id = send_basket_keyboard(bot, chat_id)
                buket_text = buketText(chat_id)
                buket_text = buket_text[0:-2]
                if buket_text == "0":
                    bot.sendMessage(chat_id, text='Ваша корзина пуста', parse_mode=bot.PARSE_MODE_MARKDOWN)
                else:
                    basket_list(bot, chat_id, message_id)
                    payment_fun(bot, chat_id)
            elif 'Очистить корзину' in text:
                basket.objects.filter(chatid=chat_id).delete()
                send_start_keyboard(bot, chat_id)
            elif text in ['Список товаров в корзине']:
                message_id = send_basket_keyboard(bot, chat_id)
                basket_list(bot, chat_id, message_id)
            elif text in ['Статус заказов']:
                status_of_orders(bot, chat_id)
            elif text in ['Архив прошлых заказов']:
                archive_orders(bot, chat_id)
            elif text in ['Предидущие товары', 'Предидущие акции']:
                if UseCategory.objects.filter(chatid=chat_id).exists():
                    globall = globall - 10
                    next_product(bot, chat_id, globall)
            elif text in ['Следующие товары', 'Следующие акции']:
                if UseCategory.objects.filter(chatid=chat_id).exists():
                    globall =  globall + 10
                    next_product(bot, chat_id, globall)
            elif 'Подкатегория:' in text:
                text = text[14:]
                send_subcategory_keyboard(bot, chat_id, text, 0)
            else:
                if Категория.objects.filter(Имя=text).exists():
                    send_category_keyboard(bot, chat_id, text, 0)

        if handler[0].handler == "1":
            x = UseCategory.objects.filter(chatid=chat_id)
            x = x[0]
            x.telephone = text
            x.handler = 0
            y = addresses(chatid=chat_id, address=x.address, name = x.name, telephone = text)
            x.save()
            y.save()

            addresses_id = str(y.id)
            #вызывать тут
            price = buketText(chat_id)
            price = price[0:-2]
            if price == "0":
                bot.sendMessage(chat_id, text='Ваша корзина пуста', parse_mode=bot.PARSE_MODE_MARKDOWN)
            else:
                payer(bot, chat_id, addresses_id)
            #в неё отправлять id addresses, chat id(нынешнюю корзину, цену)

            



        if handler[0].handler == "2":
            if UseCategory.objects.filter(chatid=chat_id).exists():
                x = UseCategory.objects.filter(chatid=chat_id)
                x = x[0]
                x.name = text
                x.handler = 1
                x.save()
            bot.sendMessage(chat_id, text='Введите номер телефона:', parse_mode=bot.PARSE_MODE_MARKDOWN)

        if handler[0].handler == "3":
            if UseCategory.objects.filter(chatid=chat_id).exists():
                x = UseCategory.objects.filter(chatid=chat_id)
                x = x[0]
                x.address = text
                x.handler = 2
                x.save()
            bot.sendMessage(chat_id, text='Введите имя:', parse_mode=bot.PARSE_MODE_MARKDOWN)
# обработчик отправленных пользователем сообщений(кнопок меню)


# все что связанно с кнопками под сообщениями
@processor(state_manager, from_states=state_types.All, update_types=[update_types.CallbackQuery])
def handle_callback_query(bot: TelegramBot, update, state):
    callback_data = update.get_callback_query().get_data()
    callback_data = callback_data.split()
    """
    в калбек приходит строка, и разбивается на массив слов
    вычисляется длина массива (len(callback_data)) и по ней определяется то,
    как обрабатывать этот масив
    и какие действия предпринять
    """
    if len(callback_data) == 1:
        callback_data = callback_data#ничего не делающая строка, чтоб заполнить полость
    elif len(callback_data) == 2:
        if callback_data[1] == "Оплатить":
            user_info(bot, callback_data[0])
            bot.answerCallbackQuery(update.get_callback_query().get_id(), text="")
        else:
            chat_id = callback_data[0]
            product_id = callback_data[1]
            y = Продукт.objects.filter(id=product_id).filter(Отключить_продукт="0")
            if len(y) != 0:
                # запись в тех таблицу бд
                if basket.objects.filter(chatid=chat_id).filter(productid=product_id).filter(action="0").exists():
                    x = basket.objects.filter(chatid=chat_id).filter(productid=product_id).filter(action="0")
                    x = x[0]
                    x.quantity = str(int(x.quantity) + 1)
                    x.save()
                else:   
                    x = basket(chatid=chat_id, productid=product_id, quantity = 1, action = 0)
                    x.save()
                # запись в тех таблицу бд конец
                bot.answerCallbackQuery(update.get_callback_query().get_id(), text="товар добавлен в корзину")
            else: 
                bot.answerCallbackQuery(update.get_callback_query().get_id(), text="товар удален или временно недоступен")
    elif len(callback_data) == 3:
        if callback_data[2] == "Идентификатор1":
            # вызывать тут
            handler0(callback_data[0])
            price = buketText(callback_data[0])
            price = price[0:-2]
            if price == "0":
                bot.sendMessage(callback_data[0], text='Ваша корзина пуста', parse_mode=bot.PARSE_MODE_MARKDOWN)
            else:
                payer(bot, callback_data[0], callback_data[1])
        elif callback_data[2] == "Идентификатор2":

            if orders.objects.filter(id=callback_data[1]).exists():
                order = orders.objects.filter(id=callback_data[1])
                order = order[0].date

                if buket_arhiv.objects.filter(date=order).filter(chatid=callback_data[0]).exists():
                    x = buket_arhiv.objects.filter(date=order).filter(chatid=callback_data[0])
                    basket.objects.filter(chatid=callback_data[0]).delete()
                    for el in x:
                        y = basket(chatid=el.chatid, productid=el.productid, quantity = el.quantity, action = el.action)
                        y.save()


                
                bot.sendMessage(callback_data[0], text='Заказ добавлен в корзину', parse_mode=bot.PARSE_MODE_MARKDOWN)
            else:
                bot.sendMessage(callback_data[0], text='Неизвестная ошибка', parse_mode=bot.PARSE_MODE_MARKDOWN)
            bot.answerCallbackQuery(update.get_callback_query().get_id(), text="")
        else:
            chat_id = callback_data[0]
            product_id = callback_data[1]
            y = Акции.objects.filter(id=product_id).filter(Отключить_акцию="0")
            y = action_data_filtr(y)
            if len(y) != 0:
                # запись в тех таблицу бд
                if basket.objects.filter(chatid=chat_id).filter(productid=product_id).filter(action="1").exists():
                    x = basket.objects.filter(chatid=chat_id).filter(productid=product_id).filter(action="1")
                    x = x[0]
                    x.quantity = str(int(x.quantity) + 1)
                    x.save()
                else:   
                    x = basket(chatid=chat_id, productid=product_id, quantity = 1, action = 1)
                    x.save()
                # запись в тех таблицу бд конец
                bot.answerCallbackQuery(update.get_callback_query().get_id(), text="акция добавлена в корзину")
            else:
                bot.answerCallbackQuery(update.get_callback_query().get_id(), text="акция не действует")
    elif len(callback_data) == 5:
        from_basket_del(callback_data, bot)
        bot.answerCallbackQuery(update.get_callback_query().get_id(), text="удалено")
# все что связанно с кнопками под сообщениями


#функция срабатывает когда юзер тыкает подкатегорию 
def send_subcategory_keyboard(bot, chat_id, subcategory, globall):
    if Подкатегория.objects.filter(Имя=subcategory).exists():
        # маленький кусочек определяющий кнопки
        buket_text = buketText(chat_id)
        bot.sendMessage(
            chat_id,
            text=subcategory,
            reply_markup=ReplyKeyboardMarkup.a(
                one_time_keyboard=True,
                resize_keyboard=True,
                keyboard=[
                    [KeyboardButton.a('Предидущие товары')],
                    [KeyboardButton.a('Следующие товары')],
                    # [KeyboardButton.a('Поиск товара (по ид)')],
                    [KeyboardButton.a('Личный кабинет')],
                    [KeyboardButton.a('В начало'), KeyboardButton.a('Корзина (' + buket_text + ')')],
                    [KeyboardButton.a('Акции')
                    # , KeyboardButton.a('Оператор')
                    ],
                ]
            )
        )
        # весь остаток функции вывод товаров
        records = UseCategory.objects.filter(chatid=chat_id)
        category_id = records[0].category #помнит в какой юзер категории
        records = Подкатегория.objects.filter(Категория=category_id).filter(Имя=subcategory)
        records = records[0].id #помнит в какой юзер подкатегории
        subcategory_id = records #помнит в какой юзер подкатегории
        all_records = Продукт.objects.filter(Подкатегория=subcategory_id).filter(Отключить_продукт="0")
        # обработчик исключений
        records = all_records[globall:globall+10] #выборка с нынешним значением глобал
        count = int(len(records)) #длина выборки
        if count > 0: #если выборка существует все ок
            globall = globall # и модуль ничего не делает
        else: 
            globall = globall - 10 #иначе проверяется вышел ли пользователь через верхнюю границу списка
            if globall < 0: #на случай если список просто был пустым
                globall = 0
            records = all_records[globall:globall+10] #присваивается корректное значение или 0
        if globall < 0: #вообще не обязателен, но я не уверен что нигде не упустил нюанса
            globall = 0
        # обработчик исключений
        # запись в тех таблицу бд
        if UseCategory.objects.filter(chatid=chat_id).exists():
            x = UseCategory.objects.filter(chatid=chat_id)
            x = x[0]
            x.subcategory = subcategory
            x.globall=globall
            x.save()
        else:   
            x = UseCategory(chatid=chat_id, category=category_id, subcategory = subcategory, globall=0)
            x.save()
        # запись в тех таблицу бд конец
        pass_product(records, bot, chat_id)
    else:
        send_start_keyboard(bot, chat_id)
#функция срабатывает когда юзер тыкает подкатегорию 


#функция срабатывает когда юзер тыкает категорию 
def send_category_keyboard(bot, chat_id, text, globall):
    records = Категория.objects.filter(Имя=str(text))
    category_name = records[0]
    category_id = records[0].id
    records = Подкатегория.objects.filter(Категория=category_id)
    count = int(len(records))
    i=0
    buket_text = buketText(chat_id)
    menu = [
        ]
    if count > 0:
        while i < count:
            menu = menu +[ [KeyboardButton.a("Подкатегория: " + str(records[i]))], ]
            i=i+1
        records = []
    else:
        all_records = Продукт.objects.filter(Категория=category_id).filter(Отключить_продукт="0")
        # обработчик исключений
        records = all_records[globall:globall+10] #выборка с нынешним значением глобал
        count = int(len(records)) #длина выборки
        if count > 0: #если выборка существует все ок
            globall = globall # и модуль ничего не делает
        else: 
            globall = globall - 10 #иначе проверяется вышел ли пользователь через верхнюю границу списка
            if globall < 0: #на случай если список просто был пустым
                globall = 0
            records = all_records[globall:globall+10] #присваивается корректное значение или 0
        if globall < 0: #вообще не обязателен, но я не уверен что нигде не упустил нюанса
            globall = 0
        # обработчик исключений
        menu = menu + [ [KeyboardButton.a('Предидущие товары')], [KeyboardButton.a('Следующие товары')],]
    menu = menu + [
            [KeyboardButton.a('Личный кабинет')],
            [KeyboardButton.a('В начало'), KeyboardButton.a('Корзина (' + buket_text + ')')],
            [KeyboardButton.a('Акции')
            # , KeyboardButton.a('Оператор')
            ],
        ]
    bot.sendMessage(
        chat_id,
        text='Категория (' + str(category_name) + ')',
        reply_markup=ReplyKeyboardMarkup.a(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=menu
        )
    )
    # запись в тех таблицу бд
    if UseCategory.objects.filter(chatid=chat_id).exists():
        x = UseCategory.objects.filter(chatid=chat_id)
        x = x[0]
        x.category = category_id
        x.subcategory = 1
        x.globall = globall
        x.save()
    else:   
        x = UseCategory(chatid=chat_id, category=category_id, subcategory = 1, globall=globall)
        x.save()
    # запись в тех таблицу бд конец
    pass_product(records, bot, chat_id)
#функция срабатывает когда юзер тыкает категорию


# стартовая клавиатура 
def send_start_keyboard(bot, chat_id):
    buket_text = buketText(chat_id)
    bot.sendMessage(
        chat_id,
        text='Вы перешли в начальный раздел',
        reply_markup=ReplyKeyboardMarkup.a(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton.a('Выбрать товар')],
                # [KeyboardButton.a('Поиск товара (по ид)')],
                [KeyboardButton.a('Личный кабинет')],
                [KeyboardButton.a('В начало'), KeyboardButton.a('Корзина (' + buket_text + ')')],
                [KeyboardButton.a('Акции')
                # , KeyboardButton.a('Оператор')
                ],
            ]
        )
    )
# стартовая клавиатура 


# вызывается при нажатии кнопки 'Выбрать товар'
def send_tovar_keyboard(bot, chat_id):
    records = Категория.objects.all()
    leng = int(len(records))
    i=0
    # генерация переменной menu отвечающей за кнопки
    menu = [
        ]
    while i < leng:
        menu = menu + [ [KeyboardButton.a(str(records[i]))], ]
        i=i+1
    buket_text = buketText(chat_id)
    menu = menu + [
            [KeyboardButton.a('Личный кабинет')],
            [KeyboardButton.a('В начало'), KeyboardButton.a('Корзина (' + buket_text + ')')],
            [KeyboardButton.a('Акции')
            # , KeyboardButton.a('Оператор')
            ],
        ]
    # генерация переменной menu отвечающей за кнопки
    bot.sendMessage(
        chat_id,
        text='Выбор категории',
        reply_markup=ReplyKeyboardMarkup.a(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=menu
        )
    )
# вызывается при нажатии кнопки 'Выбрать товар'


# вызывается при нажатии кнопки личный кабинет
def send_lk_keyboard(bot, chat_id):
    buket_text = buketText(chat_id)
    bot.sendMessage(
        chat_id,
        text='Вы перешли в личный кабинет',
        reply_markup=ReplyKeyboardMarkup.a(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton.a('Статус заказов')],
                [KeyboardButton.a('Архив прошлых заказов')],
                [KeyboardButton.a('Личный кабинет')],
                [KeyboardButton.a('В начало'), KeyboardButton.a('Корзина (' + buket_text + ')')],
                [KeyboardButton.a('Акции')
                # , KeyboardButton.a('Оператор')
                ],
            ]
        )
    )
# вызывается при нажатии кнопки личный кабинет


# вызывается при нажатии кнопки корзина(возращает id сообщения 'Корзина')
def send_basket_keyboard(bot, chat_id):
    buket_text = buketText(chat_id)
    message = bot.sendMessage(
        chat_id,
        text='Корзина',
        reply_markup=ReplyKeyboardMarkup.a(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton.a('Оплатить: ' + buket_text)],
                [KeyboardButton.a('Список товаров в корзине')],
                [KeyboardButton.a('Очистить корзину')],
                [KeyboardButton.a('Личный кабинет')],
                [KeyboardButton.a('В начало'), KeyboardButton.a('Корзина (' + buket_text + ')')],
                [KeyboardButton.a('Акции')
                # , KeyboardButton.a('Оператор')
                ],
            ]
        )
    )
    return message.message_id
# вызывается при нажатии кнопки корзина(возращает id сообщения 'Корзина')


# предидущие/следующие товары
def next_product(bot, chat_id, globall):
    x = UseCategory.objects.filter(chatid=chat_id)
    if globall < 0:
            globall = 0
    if x[0].subcategory == "1":
        if x[0].category == "1":
            action(bot, chat_id, globall)
        else:
            text = Категория.objects.filter(id=str(x[0].category))
            text = text[0].Имя
            send_category_keyboard(bot, chat_id, text, globall)
    else:
        text = UseCategory.objects.filter(chatid=chat_id)
        text = text[0].subcategory
        send_subcategory_keyboard(bot, chat_id, text, globall)
# предидущие/следующие товары


# вывод товаров
def pass_product(records, bot, chat_id):
    i=0
    value = 10
    if value > len(records):
        value = len(records)
    while i < value:
        text = records[i].Имя + '\n' + records[i].Описание + '\n' + records[i].Цена + ' р.'
        if hasattr(records[i], 'Отключить_акцию'):
            callback_data = chat_id+" "+str(records[i].id)+" Акция"
        else:
            callback_data = chat_id+" "+str(records[i].id)
        bot.sendPhoto(
            chat_id, 
            'https://bot.workhunt.ru/' + str(records[i].Фото), 
            caption=text,
            # text,
            reply_markup=InlineKeyboardMarkup.a(
                inline_keyboard=[
                    [
                        InlineKeyboardButton.a('Добавить в корзину', callback_data=callback_data),
                    ]
                ]
            )
        );
        i=i+1
# вывод товаров


# определяет количество товаров в корзине
def buketText(chat_id):
    buket_text = 0
    records_bascet = basket.objects.filter(chatid=chat_id).filter(action="0")
    # all_product = basket.objects.filter(chatid=chat_id)
    x = len(records_bascet)
    i = 0
    while i < x:
        if Продукт.objects.filter(id=records_bascet[i].productid).filter(Отключить_продукт="0").exists():
            y = []
            y = Продукт.objects.filter(id=records_bascet[i].productid).filter(Отключить_продукт="0")
            y = int(y[0].Цена)
            y = int(records_bascet[i].quantity) * y
            buket_text = buket_text + y
        i=i+1

    records_bascet = basket.objects.filter(chatid=chat_id).filter(action="1")
    x =len(records_bascet)
    i = 0
    while i < x:
        if Акции.objects.filter(id=records_bascet[i].productid).filter(Отключить_акцию="0").exists():
            y = []
            y = Акции.objects.filter(id=records_bascet[i].productid).filter(Отключить_акцию="0")
            y = action_data_filtr(y)
            if len(y) != 0:
                y = int(y[0].Цена)
                y = int(records_bascet[i].quantity) * y
                buket_text = buket_text + y
        i=i+1
    buket_text = str(buket_text) + "р."
    return buket_text
# определяет количество товаров в корзине


# показывает товары в корзине
def basket_list(bot, chat_id, message_id):
    records_bascet = basket.objects.filter(chatid=chat_id).filter(action="0")
    i=0
    value = len(records_bascet)
    while i < value:
        if Продукт.objects.filter(id=records_bascet[i].productid).filter(Отключить_продукт="0").exists():
            message_id_get = str(int(message_id) + i + 1)
            records_product = Продукт.objects.filter(id=records_bascet[i].productid).filter(Отключить_продукт="0")
            bascet_id = records_bascet[i].id
            text = records_product[0].Имя + '  ' + records_product[0].Цена  + 'р.  ' + records_bascet[i].quantity + 'шт.'
            bot.sendMessage(
                chat_id, 
                text=text,
                reply_markup=InlineKeyboardMarkup.a(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton.a('Удалить 1 шт', callback_data=chat_id+" "+str(records_bascet[i].id) +" "+ '1del' +" "+ message_id_get+" "+str(bascet_id)),
                            InlineKeyboardButton.a('Удалить все', callback_data=chat_id+" "+str(records_bascet[i].id) +" "+ 'delall' +" "+ message_id_get+" "+str(bascet_id)),
                        ]
                    ]
                )
                )
        i=i+1


    message_id = int(message_id) + i
    records_bascet = basket.objects.filter(chatid=chat_id).filter(action="1")
    i=0
    value = len(records_bascet)
    while i < value:
        if Акции.objects.filter(id=records_bascet[i].productid).filter(Отключить_акцию="0").exists():
            message_id_get = str(int(message_id) + i + 1)
            records_product = Акции.objects.filter(id=records_bascet[i].productid).filter(Отключить_акцию="0")
            records_product = action_data_filtr(records_product)
            if len(records_product) != 0:
                bascet_id = records_bascet[i].id
                text = records_product[0].Имя + '  ' + records_product[0].Цена  + 'р.  ' + records_bascet[i].quantity + 'шт.'
                bot.sendMessage(
                    chat_id, 
                    text=text,
                    reply_markup=InlineKeyboardMarkup.a(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton.a('Удалить 1 шт', callback_data=chat_id+" "+str(records_bascet[i].id) +" "+ '1del' +" "+ message_id_get+" "+str(bascet_id)),
                                InlineKeyboardButton.a('Удалить все', callback_data=chat_id+" "+str(records_bascet[i].id) +" "+ 'delall' +" "+ message_id_get+" "+str(bascet_id)),
                            ]
                        ]
                    )
                    )
        i=i+1
# показывает товары в корзине


# удаляет товары из корзины
def from_basket_del(callback_data, bot):
    chat_id = callback_data[0]
    product_id = callback_data[1]
    del1_delall = callback_data[2]
    message_id = callback_data[3]
    bascet_id = callback_data[4]
    if basket.objects.filter(chatid=chat_id).filter(id=product_id).exists():
        records_bascet = basket.objects.filter(id=bascet_id)
        # records_product = Продукт.objects.filter(id=records_bascet[0].productid).filter(Отключить_продукт="0")

        pal1 = basket.objects.filter(chatid=chat_id).filter(id=product_id)
        if pal1[0].action:
            records_product = Акции.objects.filter(id=records_bascet[0].productid).filter(Отключить_акцию="0")
            records_product = action_data_filtr(records_product)
        else:
            records_product = Продукт.objects.filter(id=records_bascet[0].productid).filter(Отключить_продукт="0")

        
        if len(records_product) != 0:
            text = records_product[0].Имя + '  ' + records_product[0].Цена  + 'р.  ' + str(int(records_bascet[0].quantity)-1) + 'шт.'
            records = basket.objects.filter(chatid=chat_id).filter(id=product_id)
            records = records[0]
            records.quantity = str(int(records.quantity) - 1)
            records.save()
            if del1_delall == "delall":
                bot.deleteMessage(chat_id=chat_id, message_id=message_id)
                basket.objects.filter(chatid=chat_id).filter(id=product_id).delete()
            bot.editMessageText (
                chat_id=chat_id, 
                message_id=message_id, 
                text=text,
                reply_markup=InlineKeyboardMarkup.a(
                    inline_keyboard=[
                        [
                            InlineKeyboardButton.a('Удалить 1 шт', callback_data=chat_id+" "+product_id+" "+ '1del' +" "+ message_id+" "+ bascet_id),
                            InlineKeyboardButton.a('Удалить все', callback_data=chat_id+" "+product_id+" "+ 'delall' +" "+ message_id+" "+ bascet_id),
                        ]
                    ]
                ))
            if records.quantity == "0":
                bot.deleteMessage(chat_id=chat_id, message_id=message_id)
                basket.objects.filter(chatid=chat_id).filter(id=product_id).delete()
# удаляет товары из корзины


# вызывается при нажатии кнопки акции
def action(bot, chat_id, globall):
    buket_text = buketText(chat_id)
    bot.sendMessage(
        chat_id,
        text='Вы перешли в список акций',
        reply_markup=ReplyKeyboardMarkup.a(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton.a('Предидущие акции')], 
                [KeyboardButton.a('Следующие акции')],
                # [KeyboardButton.a('Поиск товара (по ид)')],
                [KeyboardButton.a('Личный кабинет')],
                [KeyboardButton.a('В начало'), KeyboardButton.a('Корзина (' + buket_text + ')')],
                [KeyboardButton.a('Акции')
                # , KeyboardButton.a('Оператор')
                ],
            ]
        )
    )
    records = Акции.objects.filter(Отключить_акцию="0")
    all_records = action_data_filtr(records)
    
    # обработчик исключений
    records = all_records[globall:globall+10] #выборка с нынешним значением глобал
    count = int(len(records)) #длина выборки
    if count > 0: #если выборка существует все ок
        globall = globall # и модуль ничего не делает
    else: 
        globall = globall - 10 #иначе проверяется вышел ли пользователь через верхнюю границу списка
        if globall < 0: #на случай если список просто был пустым
            globall = 0
        records = all_records[globall:globall+10] #присваивается корректное значение или 0
    if globall < 0: #вообще не обязателен, но я не уверен что нигде не упустил нюанса
        globall = 0
    # обработчик исключений
    # запись в тех таблицу бд
    if UseCategory.objects.filter(chatid=chat_id).exists():
        x = UseCategory.objects.filter(chatid=chat_id)
        x = x[0]
        x.category=1
        x.subcategory = 1
        x.globall=globall
        x.save()
    else:   
        x = UseCategory(chatid=chat_id, category=1, subcategory = 1, globall=0)
        x.save()
    # запись в тех таблицу бд конец
    pass_product(records, bot, chat_id)
# вызывается при нажатии кнопки акции


# вызывается при нажатии кнопки оплатить
def payment_fun(bot, chat_id):
    buket_text = buketText(chat_id)
    bot.sendMessage(
        chat_id,
        text='⬆Ваши товары⬆',
        reply_markup=ReplyKeyboardMarkup.a(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton.a('Выбрать товар')],
                # [KeyboardButton.a('Поиск товара (по ид)')],
                [KeyboardButton.a('Личный кабинет')],
                [KeyboardButton.a('В начало'), KeyboardButton.a('Корзина (' + buket_text + ')')],
                [KeyboardButton.a('Акции')
                # , KeyboardButton.a('Оператор')
                ],
            ]
        )
    )
    text = 'Итоговая цена: ' + buket_text
    bot.sendMessage(
            chat_id, 
            text=text,
            reply_markup=InlineKeyboardMarkup.a(
                inline_keyboard=[
                    [
                        InlineKeyboardButton.a('Оплатить заказ', callback_data=chat_id + " Оплатить"),
                        # InlineKeyboardButton.a('Связатся с оператором', callback_data=chat_id),
                    ]
                ]
            )
            )
# вызывается при нажатии кнопки оплатить


# вызывается при нажатии кнопки оплатить заказ
def user_info(bot, chat_id):
    buket_text = buketText(chat_id)
    bot.sendMessage(
        chat_id,
        text='Ваши адреса:',
        reply_markup=ReplyKeyboardMarkup.a(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton.a('Отмена')],
                # [KeyboardButton.a('Поиск товара (по ид)')],
                [KeyboardButton.a('Личный кабинет')],
                [KeyboardButton.a('В начало'), KeyboardButton.a('Корзина (' + buket_text + ')')],
                [KeyboardButton.a('Акции')
                # , KeyboardButton.a('Оператор')
                ],
            ]
        )
    )
    # вывод последних 5 адресов
    addresses_get = addresses.objects.filter(chatid=chat_id)
    i=len(addresses_get)
    if i>0:
        if i>5:
            i = i - 5
            addresses_get = addresses_get[i:]
        i=0

        while i < len(addresses_get):
            addresses_id = addresses_get[i].id
            text = addresses_get[i].address + '\n' + addresses_get[i].name + '\n' + addresses_get[i].telephone
            bot.sendMessage(
                    chat_id, 
                    text=text,
                    reply_markup=InlineKeyboardMarkup.a(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton.a('Выбрать адрес', callback_data=chat_id + " " + str(addresses_id) + " Идентификатор1"), 
                            ]
                        ]
                    )
                    )
            i=i+1
    # вывод последних 5 адресов
    bot.sendMessage(chat_id, text='Или введите новый адрес доставки:')
    # запись в тех таблицу бд
    if UseCategory.objects.filter(chatid=chat_id).exists():
        x = UseCategory.objects.filter(chatid=chat_id)
        x = x[0]
        x.handler = 3
        x.save()
    # запись в тех таблицу бд конец
# вызывается при нажатии кнопки оплатить заказ


# отменяет сбор данных пользователя
def handler0(chat_id):
    # запись в тех таблицу бд
    if UseCategory.objects.filter(chatid=chat_id).exists():
        x = UseCategory.objects.filter(chatid=chat_id)
        x = x[0]
        x.handler = 0
        x.save()
    else:
        x = UseCategory(chatid=chat_id, category=1, subcategory = 1, globall=0)
        x.save()
    # запись в тех таблицу бд конец
# отменяет сбор данных пользователя


# создает и отправляет ссылку для оплаты
def payer(bot, chat_id, addresses_id):
    # https://b24-dcnmqd.bitrix24.ru/rest/1/oygxu7dzbn6fszbh/crm.deal.add.json?fields[TITLE]=fcygu&fields[STAGE_ID]=NEW&fields[OPPORTUNITY]=1000&fields[CURRENCY_ID]=RUB&fields[TYPE_ID]=GOODS&fields[ADDITIONAL_INFO]=hhhhhhhhhhh&fields[COMMENTS]=gfhdgfhdrtfyrdehtrh
    # https://b24-dcnmqd.bitrix24.ru/rest/1/oygxu7dzbn6fszbh/crm.deal.add.json
    address = addresses.objects.filter(id=addresses_id)
    address = address[0]
    buket = basket.objects.filter(chatid=chat_id)
    text = "Адрес:" + '\n' + address.address +" Имя:"+ address.name +" Телефон:"+ address.telephone

    buket_text = buketText(chat_id)
    price = buket_text[0:-2]
    # URL, на который собираетесь отправлять запрос
    url = settings.WEBHOOK_B24 + "crm.deal.add.json"
    # Параметры запроса
    params = [{ 
        'fields[TITLE]': 'Заказ: ' + address.telephone, 
        'fields[TYPE_ID]': 'GOODS', 
        'fields[STAGE_ID]': 'NEW', 
        'fields[CURRENCY_ID]': 'RUB', 
        'fields[OPPORTUNITY]': price,
        'fields[COMMENTS]': text,				
    },]
    # сам запрос
    r = requests.get(url=url, params=params[0])
    r = r.json()
    r = r['result']

    params ={
        'id': r, 		
    }
    i=0
    for el in buket:
        if el.action:
            if Акции.objects.filter(id=el.productid).filter(Отключить_акцию="0").exists():
                produkt = Акции.objects.filter(id=el.productid).filter(Отключить_акцию="0")
                produkt = action_data_filtr(produkt)
                if len(produkt) != 0:
                    produkt = produkt[0]
                    params_i = { 
                    'rows['+str(i)+'][PRODUCT_NAME]': produkt.Имя, 
                    'rows['+str(i)+'][PRICE]': produkt.Цена, 
                    'rows['+str(i)+'][QUANTITY]': el.quantity,
                    }
                    params={**params, **params_i}
        else:
            if Продукт.objects.filter(id=el.productid).filter(Отключить_продукт="0").exists():
                produkt = Продукт.objects.filter(id=el.productid).filter(Отключить_продукт="0")
                produkt = produkt[0]
                params_i = { 
                    'rows['+str(i)+'][PRODUCT_NAME]': produkt.Имя, 
                    'rows['+str(i)+'][PRICE]': produkt.Цена, 
                    'rows['+str(i)+'][QUANTITY]': el.quantity,
                }
                params={**params, **params_i}
        i=i+1

    
        
    # URL, на который собираетесь отправлять запрос
    url = settings.WEBHOOK_B24 + "crm.deal.productrows.set"
    # Параметры запроса
    params = [params,]
    # сам запрос
    paralimpiec = requests.get(url=url, params=params[0])
    # {"result":105,"time":{"start":1644309831.906244,"finish":1644309832.1214111,"duration":0.21516704559326172,"processing":0.188059
    paralimpiec.json()
    
    
    Configuration.account_id = settings.YOOKASSA_ID
    Configuration.secret_key = settings.YOOKASSA_KEY
    r2 = "Заказ №" + str(r)
    payment = Payment.create({
        "amount": {
            "value": price,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://bot.workhunt.ru/"
        },
        "capture": True,
        "description": r2
    }, uuid.uuid4())


    # запись в тех таблицу бд
    date_key = datetime.datetime.now()#.timestamp()
    x = orders(chatid=chat_id, date=date_key, faze = 0, address_id = addresses_id, CRM = r, youMoneyId = payment.id)
    x.save()
    for el in buket:
        y = buket_arhiv(chatid=chat_id, date=date_key, productid = el.productid, quantity=el.quantity, action=el.action)
        y.save()
    # запись в тех таблицу бд конец
    # очистка корзины
    basket.objects.filter(chatid=chat_id).delete()
    # очистка корзины
    # можно убрать, лишний раз обновляет цену возле кнопки карзины
    buket_text = buketText(chat_id)
    # можно убрать, лишний раз обновляет цену возле кнопки карзины




    bot.sendMessage(
        chat_id,
        text=payment.confirmation.confirmation_url,
        reply_markup=ReplyKeyboardMarkup.a(
            one_time_keyboard=True,
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton.a('Выбрать товар')],
                # [KeyboardButton.a('Поиск товара (по ид)')],
                [KeyboardButton.a('Личный кабинет')],
                [KeyboardButton.a('В начало'), KeyboardButton.a('Корзина (' + buket_text + ')')],
                [KeyboardButton.a('Акции')
                # , KeyboardButton.a('Оператор')
                ],
            ]
        )
    )
# создает и отправляет ссылку для оплатыя


#выводит статус заказов
def status_of_orders(bot, chat_id):
    buket_text = buketText(chat_id)
    # faze="1" товар оплачен
    # faze="2" товар в пути
    order = orders.objects.filter(chatid=chat_id).filter(faze="2") | orders.objects.filter(chatid=chat_id).filter(faze="3")
    bot.sendMessage(
            chat_id,
            text="Статус ваших заказов:",
            reply_markup=ReplyKeyboardMarkup.a(
                one_time_keyboard=True,
                resize_keyboard=True,
                keyboard=[
                    [KeyboardButton.a('Статус заказов')],
                    [KeyboardButton.a('Архив прошлых заказов')],
                    [KeyboardButton.a('Личный кабинет')],
                    [KeyboardButton.a('В начало'), KeyboardButton.a('Корзина (' + buket_text + ')')],
                    [KeyboardButton.a('Акции')
                    # , KeyboardButton.a('Оператор')
                    ],
                ]
            )
        )
    for el in order:
        address = addresses.objects.filter(id=el.address_id)
        if el.faze == "2":
            text = "Заказ: " + address[0].address + '\n' + "Статус: Оплачено"+ '\n' + '\n'
        else:
            text = "Заказ: " + address[0].address + '\n' + "Статус: Доставляется"+ '\n' + '\n'
        price = 0
        product = buket_arhiv.objects.filter(date=el.date).filter(chatid=chat_id)
        for el2 in product:  
            if el2.action:
                records_product = Акции.objects.filter(id=el2.productid).filter(Отключить_акцию="0")
                records_product = action_data_filtr(records_product)
                if len(records_product) != 0:
                    text = text + records_product[0].Имя + '  ' + records_product[0].Цена  + 'р.  ' + el2.quantity + 'шт.' + '\n'
            else:
                records_product = Продукт.objects.filter(id=el2.productid).filter(Отключить_продукт="0")
                text = text + records_product[0].Имя + '  ' + records_product[0].Цена  + 'р.  ' + el2.quantity + 'шт.' + '\n'
            price = int(records_product[0].Цена) * int(el2.quantity) + price
        text = text + '\n' +"Цена: "+ str(price) + "р."
        bot.sendMessage(chat_id, text=text)
#выводит статус заказов


#выводит архив заказов
def archive_orders(bot, chat_id):
    buket_text = buketText(chat_id)
    # faze="3" товар доставлен
    order = orders.objects.filter(chatid=chat_id).filter(faze="4")
    bot.sendMessage(
            chat_id,
            text="Архив заказов:",
            reply_markup=ReplyKeyboardMarkup.a(
                one_time_keyboard=True,
                resize_keyboard=True,
                keyboard=[
                    [KeyboardButton.a('Статус заказов')],
                    [KeyboardButton.a('Архив прошлых заказов')],
                    [KeyboardButton.a('Личный кабинет')],
                    [KeyboardButton.a('В начало'), KeyboardButton.a('Корзина (' + buket_text + ')')],
                    [KeyboardButton.a('Акции')
                    # , KeyboardButton.a('Оператор')
                    ],
                ]
            )
        )
    for el in order:
        address = addresses.objects.filter(id=el.address_id)
        text = "Заказ №"+ el.CRM + '\n' + '\n'
        price = 0
        product = buket_arhiv.objects.filter(date=el.date).filter(chatid=chat_id)
        for el2 in product:  
            if el2.action:
                records_product = Акции.objects.filter(id=el2.productid).filter(Отключить_акцию="0")
                records_product = action_data_filtr(records_product)
                if len(records_product) != 0:
                    text = text + records_product[0].Имя + '  ' + records_product[0].Цена  + 'р.  ' + el2.quantity + 'шт.' + '\n'
            else:
                records_product = Продукт.objects.filter(id=el2.productid).filter(Отключить_продукт="0")
                text = text + records_product[0].Имя + '  ' + records_product[0].Цена  + 'р.  ' + el2.quantity + 'шт.' + '\n'
            price = int(records_product[0].Цена) * int(el2.quantity) + price
        text = text + '\n' +"Цена: "+ str(price) + "р."
        bot.sendMessage(
            chat_id, 
            text=text,
            reply_markup=InlineKeyboardMarkup.a(
                inline_keyboard=[
                    [
                        InlineKeyboardButton.a('Повторить заказ', callback_data=chat_id+" "+str(el.id)+" Идентификатор2"),
                    ]
                ]
            ))
#выводит архив заказов

# фильтр акций по дате
def action_data_filtr(records):
    # сюда приходит масив акций не отфильтрованный по дате
    # возвращается только с актуальной датой
    count = int(len(records))
    all_records = []
    i=0
    while i < count:
        if records[i].Дата_начала == None:
            all_records = all_records + [records[i]]
        elif records[i].Дата_окончания == None:
            all_records = all_records + [records[i]]
        elif records[i].Дата_начала.timestamp() <= datetime.datetime.now().timestamp(): #True значит что акция уже началась
            if records[i].Дата_окончания.timestamp() >= datetime.datetime.now().timestamp():#True значит что акция ещё не закончилась
                all_records = all_records + [records[i]]
                # records = records
        i=i+1
    return all_records
# фильтр акций по дате
    

def Gulad():
    # print('я')
    # print(type(bot))
    # print('гуль')
    basket.objects.all().delete()
    UseCategory.objects.all().delete()
    addresses.objects.all().delete()
    orders.objects.all().delete()
    buket_arhiv.objects.all().delete()