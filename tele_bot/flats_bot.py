import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters import Text
import db_client
from config import *
from utils import *


LIST_FILTER = ["Сортировка по городу", "Сорировка по стоимости квадратного метра" ]
LIST_SITY = ["брест", "витебск", "гродно", "гомель", "минск", "могилев", "Главное меню"]




bot = Bot(API_TOKEN)   
dp = Dispatcher(bot) 

async def post_tg(message,flats):
    for post in flats:
        post_message = f'<b>Цена:</b> {post[2]} BYN\n'
        post_message += f'<b>Описание:</b> {post[6]}\n\n'
        post_message += '\n'.join(list(map(lambda el: el, post[8].split(',')[:6])))
        await bot.send_message(chat_id=message.from_user.id, text=post_message, parse_mode='html')



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    button = menu(LIST_FILTER)
    msg = await bot.send_message(chat_id= REPORT_GROUP_ID,
                           text= 'Выберите способ сортировки',
                           reply_markup=button)
    await message.delete()  
    await asyncio.sleep(10)
    try:
        await msg.delete()
    except Exception:
        print("Сообщение уже удалено")
        
    

@dp.message_handler(Text(equals="Сортировка по городу"))
async def filter_command(message: types.Message):
        button = menu(LIST_SITY) 
        msg = await bot.send_message(chat_id=REPORT_GROUP_ID,
                               text= 'Выберите город',
                               reply_markup=button)
        await message.delete()
        await asyncio.sleep(10)
        try:
            await msg.delete()
        except Exception:
            print("Сообщение уже удалено")
       
        
          
@dp.message_handler(Text(equals="Главное меню"))
async def home(message: types.Message):
        markup = menu(LIST_FILTER)        
        msg = await bot.send_message(chat_id=REPORT_GROUP_ID,
                               text="Выберите способ сортировки",
                               reply_markup=markup
                               )
        await message.delete()
        await asyncio.sleep(10)
        try:
            await msg.delete()
        except Exception:
            print("Сообщение уже удалено")
       
        
@dp.message_handler(Text(equals="Сорировка по стоимости квадратного метра"))
async def filter_flats_costs_meter(message: types.Message):
        markup = menu(LIST_FILTER)        
        msg = await bot.send_message(chat_id=REPORT_GROUP_ID,
                               text="Введите стоимость квадратного метра",
                               reply_markup=markup
                               )
        await message.delete()
        await asyncio.sleep(10)
        try:
            await msg.delete()
        except Exception:
            print("Сообщение уже удалено")
        
        
@dp.message_handler()
async def filter_flats_sity(message: types.Message):
        if message.text in LIST_SITY:
            flats = db_client.get_filter_flats(message.text, 'sity', False)
            answer_price = answer_price_meter(message.text)
            if len(flats) > 0:
                await post_tg(message,flats)
            await bot.send_message(message.from_user.id, f'Средняя цена по городу {message.text} за квадратный метр  : {answer_price}' )
            await message.delete()
        elif message.text.isdigit():
            flats = db_client.get_filter_flats(message.text, 'price', False)
            if len(flats) > 0:
                await post_tg(message,flats)
            await message.delete()
            
            
            

    
    
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates= True)
