import db_client


def answer_price_meter(sity):
    answer_price = 0
    filter_sity = db_client.get_filter_flats(sity, 'sity', False)
    for price in filter_sity:
        answer_price += price[3]
    return  answer_price / len(filter_sity)

