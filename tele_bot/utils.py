import db_client
from aiogram import types


def answer_price_meter(sity):
    answer_price = 0
    filter_sity = db_client.get_filter_flats(sity, 'sity', False)
    for price in filter_sity:
        answer_price += price[3]
    return  answer_price / len(filter_sity)

def menu(list_button=None):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    buttons = [types.KeyboardButton(x) for x in list_button]
    markup.add(*buttons)   
    return markup

def sity_list(sity_list):
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = [types.InlineKeyboardButton(text=x, callback_data=x) for x in sity_list]
    markup.add(*buttons)
    return markup


