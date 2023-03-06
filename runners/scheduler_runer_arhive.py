import schedule
import time
from constants import USED_PARSERS
from datetime import datetime
import db_client

TIME = "00:00"

def update_is_archive():
    print(f'Проверка стартовала: {datetime.now()}')
    links = USED_PARSERS[0].get_all_last_flats_links(1, 'last')
    all_is_archive = db_client.get_all_not_archive(links)
    db_client.update_is_archive_state(list(map(lambda el: el[9], all_is_archive)))
    print('Все проверено')

schedule.every().day.at(TIME).do(update_is_archive)


# while True:
#     schedule.run_pending()
#     time.sleep(1)
