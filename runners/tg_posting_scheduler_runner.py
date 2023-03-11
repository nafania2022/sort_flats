import schedule
import time
from constants import USED_PARSERS
import tg_poster
from datetime import datetime
import db_client

PARSE_EVERY_MINUTES = 1


def do_post_in_telegram():
    print(f'Телеграм оповещения стартовали: {datetime.now()}')
    parser_names = list(map(lambda el: el.get_parser_name(), USED_PARSERS))
    posts = db_client.get_all_not_posted_flats(parser_names)
    for post in posts:
        post_message = f'<b>Цена:</b> {post[2]} BYN\n'
        post_message += f'<b>Описание:</b> {post[6]}\n\n'
        post_message += '\n'.join(list(map(lambda el: el, post[8].split(',')[:6])))
        tg_poster.send_tg_post(post_message)
        
        time.sleep(5)
    db_client.update_is_posted_state(list(map(lambda el: el[9], posts)))
    
schedule.every(PARSE_EVERY_MINUTES).minutes.do(do_post_in_telegram)


while True:
    schedule.run_pending()
    time.sleep(1)
