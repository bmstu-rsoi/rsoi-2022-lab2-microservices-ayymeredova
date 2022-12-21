import psycopg2
from psycopg2 import Error

class RentalDB():
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host="postgres",
                database="rental",
                user='postgres',
                password='postgres',
                port="5432")

            self.cur = self.conn.cursor()
        except(Error, Exception) as e:
            raise(e)
        

    def check_cars_db(self, db_name):
        self.cur.execute('DROP TABLE IF EXISTS rental;')
    
        self.cur.execute("""CREATE TABLE rental
            (
        id          SERIAL PRIMARY KEY,
        rental_uid  uuid UNIQUE              NOT NULL,
        username    VARCHAR(80)              NOT NULL,
        payment_uid uuid                     NOT NULL,
        car_uid     uuid                     NOT NULL,
        date_from   TIMESTAMP WITH TIME ZONE NOT NULL,
        date_to     TIMESTAMP WITH TIME ZONE NOT NULL,
        status      VARCHAR(20)              NOT NULL
            CHECK (status IN ('IN_PROGRESS', 'FINISHED', 'CANCELED'))
        );""")

        self.cur.execute(""" INSERT INTO rental
        (
            id,
            rental_uid,
            username,
            payment_uid,
            car_uid,
            date_from,
            date_to, 
            status
        )
        VALUES(
            1,
            67ae0820-73d7-11ed-a682-00155dec5d05,
            User1,
            7ffe9644-73d0-11ed-a67f-00155dec5d05,
            2581d076-73d7-11ed-a681-00155dec5d05,
            2022-10-10,
            2022-12-12,
            IN_PROGRESS,
            );
        """)

        self.cur.execute(""" INSERT INTO rental
        (
            id,
            rental_uid,
            username,
            payment_uid,
            car_uid,
            date_from,
            date_to, 
            status
        )
        VALUES(
            1,
            a695f106-73d7-11ed-a683-00155dec5d05            
            User2,
            753f5bf8-73d0-11ed-a67e-00155dec5d05,
            d0ad8de2-73d6-11ed-a680-00155dec5d05,
            2022-01-01,
            2022-02-12,
            FINISHED,
            );
        """)


    