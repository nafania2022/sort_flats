import psycopg2
import time

DBNAME = 'postgres'
USER = 'postgresql'
PASSWORD = 'postgresql'
HOST = '127.0.0.1'


def create_flats_table():
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
            CREATE TABLE IF NOT EXISTS flats (
                id serial PRIMARY KEY,
                link CHARACTER VARYING(300) UNIQUE NOT NULL,
                reference CHARACTER VARYING(30),
                price INTEGER,
                price_meter INTEGER,
                sity CHARACTER VARYING(30),
                title CHARACTER VARYING(1000),
                description CHARACTER VARYING(3000),
                date TIMESTAMP WITH TIME ZONE,
                photo_links TEXT,
                is_tg_posted BOOLEAN,
                is_archive BOOLEAN
                )''')


def insert_flat(flat):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                INSERT INTO flats (link, reference, price, price_metre, sity, title, description, date, photo_links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
                ON CONFLICT (link) DO UPDATE 
                SET 
                link = EXCLUDED.link, 
                price = EXCLUDED.price,
                price_meter = EXCLUDED.price_meter,
                title = EXCLUDED.title, 
                description = EXCLUDED.description, 
                date = EXCLUDED.date
                 ''',
                        (flat.link, flat.reference, flat.price, flat.price_meter, flat.sity, flat.title, flat.description, flat.date,
                         ','.join(flat.images))
                        )
            
                     
def insert_flats_all(flats):
    time_start = time.time()
    all_flats = []
    for flat in flats:
        fl = []      
        fl.append(flat.link)
        fl.append(flat.reference)
        fl.append(flat.price)
        fl.append(flat.price_meter)
        fl.append(flat.sity)
        fl.append(flat.title)
        fl.append(flat.description)
        fl.append(flat.date)
        fl.append(','.join(flat.images))
        all_flats.append(tuple(fl))
    
                
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.executemany('''
                    INSERT INTO flats (link, reference, price, price_meter, sity, title, description, date, photo_links) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (link) DO UPDATE
                    set
                    link = EXCLUDED.link, 
                    price = EXCLUDED.price,
                    price_meter = EXCLUDED.price_meter,
                    sity = EXCLUDED.sity,
                    title = EXCLUDED.title, 
                    description = EXCLUDED.description, 
                    date = EXCLUDED.date
                    ''', all_flats)
            time_end = time.time() - time_start
            print("Все загружено в бд", time_end)


def get_all_not_posted_flats(parser_types):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    SELECT link, reference, price, price_meter, sity, title, description, date, photo_links, id FROM flats
                    WHERE (is_tg_posted = false or is_tg_posted IS NULL) 
                    and reference IN %(parser_types)s
                 ''',
                        {'parser_types': tuple(parser_types)}
                        )
            return cur.fetchall()


def update_is_posted_state(ids):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    UPDATE flats SET
                    is_tg_posted = true
                    WHERE id = ANY(%s)
                 ''',
                        [ids, ]
                        )
            
            
def get_all_not_archive(link):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    SELECT link, reference, price, price_meter, sity, title, description, date, photo_links, id FROM flats
                    WHERE (is_archive = false or is_archive IS NULL) 
                    and link NOT IN %(parser_link)s
                 ''',
                        {'parser_link': tuple(link)}
                        )
            return cur.fetchall()  
        
           
def update_is_archive_state(ids):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute('''
                    UPDATE flats SET
                    is_archive = true
                    WHERE id = ANY(%s)
                 ''',
                        [ids, ]
                        )
            

def get_filter_flats(sity_or_price, filter, is_archive=True):
    if filter == "sity":
        if is_archive:
            params = "sity = %(sity_or_price)s"
        else:
            params = "(is_archive = false or is_archive IS NULL) and sity = %(sity_or_price)s"
    elif filter == "price":
        if is_archive:
            params = "price_meter < %(sity_or_price)s"  
        else:
            params = "(is_archive = false or is_archive IS NULL) and price_meter < %(sity_or_price)s"
    else:
        print("Не правильные параметры ")
        return
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute(f'''
                    SELECT link, reference, price, price_meter, sity, title, description, date, photo_links, id FROM flats
                    WHERE {params} 
                 ''',
                        {'sity_or_price': sity_or_price}
                        )
            return cur.fetchall()





def test_insert(text):
    with psycopg2.connect(dbname=DBNAME, user=USER, password=PASSWORD, host=HOST) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO test (text) VALUES (%s)", text )



