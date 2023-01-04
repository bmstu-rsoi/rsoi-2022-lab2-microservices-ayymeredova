import psycopg2
from psycopg2 import Error


class PaymentDB():
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                host="postgres",
                database="payment",
                user='postgres',
                password='postgres',
                port="5432")

            self.cur = self.conn.cursor()
        except(Error, Exception) as e:
            raise(e)
        

    def check_payment_db(self, db_name):
        self.cur.execute('DROP TABLE IF EXISTS payment;')
    
        self.cur.execute("""CREATE TABLE payment
        (
            id          SERIAL PRIMARY KEY,
            payment_uid uuid        NOT NULL,
            status      VARCHAR(20) NOT NULL
                CHECK (status IN ('PAID', 'CANCELED')),
            price       INT         NOT NULL
        );""")

        self.cur.execute(""" INSERT INTO payment
        (
            id,
            payment_uid,
            status,
            price
        )
        VALUES(
            1,
            '753f5bf8-73d0-11ed-a67e-00155dec5d05',
            'PAID',
            200000
            );
        """)

        self.cur.execute(""" INSERT INTO payment
        (
            id,
            payment_uid,
            status,
            price
        )
        VALUES(
            2,
            '7ffe9644-73d0-11ed-a67f-00155dec5d05',
            'CANCELED',
            400000
            );
        """)


        self.conn.commit()

        self.cur.close()
        self.conn.close()
            