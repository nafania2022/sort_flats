from abc import ABC, abstractmethod
import db_client
import time

class ParserStandart(ABC):

    @abstractmethod
    def get_parser_name(self):
        return 'unnamed_parser'
    @abstractmethod
    def get_url(self, page_from=1):
        return

    @abstractmethod
    def get_all_last_flats_links(self, page_from=1, page_to=2):
        return []

    @abstractmethod
    def enrich_links_to_flats(self, links: list):
        return []

    @staticmethod
    def save_flats(flats):
        db_client.insert_flats_all(flats)
        # time_start = time.time()
        # for counter, flat in enumerate(flats):            
        #     print(f'Загружено в базу {counter} из {len(flats)}')
        #     db_client.insert_flat(flat)
        # time_end = time.time() - time_start
        # print(time_end)

    def update_with_last_flats(self, page_from=1, page_to=2):
        links = self.get_all_last_flats_links(page_from, page_to)
        flats = self.enrich_links_to_flats(links)
        self.save_flats(flats)
