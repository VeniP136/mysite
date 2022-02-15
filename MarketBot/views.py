from django.http import HttpResponse
import telebot
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json, requests
from MarketBot.models import Категория, Подкатегория, Продукт, UseCategory, basket, Акции, addresses, orders, buket_arhiv
from django.conf import settings
from yookassa import Payment
from venipbot.bot import TelegramBot, state_manager

botObj = TelegramBot('5049628733:AAFHDqOTl2JKqOTBM4BDkgWRJDc_hw0oHYk', state_manager)
@method_decorator(csrf_exempt)
def index(request):

    return HttpResponse("Спасибо за оплату")

@method_decorator(csrf_exempt)
def bitrix(request):
    # data = json.loads(request.body)
    # i =  str(request.body).find('5BID%5D=')
    # data = data[i+9:i+12]
    if settings.APLICATION_TOKEN == request.POST.get('auth[application_token]'):
        url = settings.WEBHOOK_B24 + "crm.deal.get"
        # Параметры запроса
        CRM_id = request.POST.get('data[FIELDS][ID]')
        params = [{ 
            'id': CRM_id,  			
        },]
        # сам запрос
        r = requests.get(url=url, params=params[0])
        r = r.json()
        r = r['result']
        r = r['STAGE_ID']
        x = orders.objects.filter(CRM=CRM_id)
        x = x[0]
        addres = addresses.objects.filter(id=x.address_id)
        if r == settings.B24_ID_NEW:
            if x.faze != "0":
                x.faze = "0"
                x.save()
                botObj.sendMessage(chat_id = x.chatid, text='Заказ №'+CRM_id+'\n'+'Адрес: '+addres[0].address+'\n'+'Статус: '+'Переведён в статус не оплаченных')
        elif r == settings.B24_ID_MANUAL:  
            if x.faze != "1":
                x.faze = "1"
                x.save()
                botObj.sendMessage(chat_id = x.chatid, text='Заказ №'+CRM_id+'\n'+'Адрес: '+addres[0].address+'\n'+'Статус: '+'Переведён в статус оплаты в ручном режиме')
        elif r == settings.B24_ID_PAID:
            if x.faze != "2":
                x.faze = "2"
                x.save()
                botObj.sendMessage(chat_id = x.chatid, text='Заказ №'+CRM_id+'\n'+'Адрес: '+addres[0].address+'\n'+'Статус: '+'Оплаченно') 
        elif r == settings.B24_ID_DELIVERED:
            if x.faze != "3":
                x.faze = "3"
                x.save()
                botObj.sendMessage(chat_id = x.chatid, text='Заказ №'+CRM_id+'\n'+'Адрес: '+addres[0].address+'\n'+'Статус: '+'Доставляется')
        elif r == settings.B24_ID_END:
            if x.faze != "4":
                x.faze = "4"
                x.save()
                botObj.sendMessage(chat_id = x.chatid, text='Заказ №'+CRM_id+'\n'+'Адрес: '+addres[0].address+'\n'+'Статус: '+'Доставлен') 
        
    return HttpResponse("Спасибо за оплату")

@method_decorator(csrf_exempt)
def payment(request):
    # settings.YOOKASSA_KEY
    data = json.loads(request.body.decode("utf-8"))
    data = data['object']
    data = data['id']
    data_id = data
    if orders.objects.filter(youMoneyId=data_id).exists():
        x = orders.objects.filter(youMoneyId=data_id)
        x = x[0]
        if x.faze == "0":
            x.faze = "2"
            data = Payment.find_one(data)
            data = data.json()
            i = data.find('"paid":')
            data = data[i+8:i+12]
            if data == "true":
                r = x.CRM
                botObj.sendMessage(chat_id = x.chatid, text='Заказ №'+ r +' оплачен')
                x.faze = "2"
                x.save()
                

                url = settings.WEBHOOK_B24 + "crm.deal.update"
                # url = settings.WEBHOOK_B24 + "crm.deal.get"
                # Параметры запроса
                params = [{ 
                    'id': r, 
                    'fields[STAGE_ID]': 'UC_UW9OK1', 			
                },]
                # сам запрос
                r = requests.get(url=url, params=params[0])
                print(r.json())


            else:
                x.faze == "0"
                x.save()
                
    else:
        print("ктото чтото мутит")
    
    return HttpResponse("хай")
# {'type': 'notification', 'event': 'payment.succeeded', 'object': {'id': '299572f4-000f-5000-9000-1af095af9464', 'status': 'succeeded', 'amount': {'value': '3.00', 'currency': 'RUB'}, 'income_amount': {'value': '2.89', 'currency': 'RUB'}, 'description': 'Заказ №181', 'recipient': {'account_id': '872149', 'gateway_id': '1937133'}, 'payment_method': {'type': 'yoo_money', 'id': '299572f4-000f-5000-9000-1af095af9464', 'saved': False, 'title': 'YooMoney wallet 410011758831136', 'account_number': '410011758831136'}, 'captured_at': '2022-02-09T06:30:06.325Z', 'created_at': '2022-02-09T06:29:08.146Z', 'test': True, 'refunded_amount': {'value': '0.00', 'currency': 'RUB'}, 'paid': True, 'refundable': True, 'metadata': {}}}

bot = telebot.TeleBot('5049628733:AAFHDqOTl2JKqOTBM4BDkgWRJDc_hw0oHYk')

