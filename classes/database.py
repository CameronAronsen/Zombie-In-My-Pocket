import sqlite3
from sqlite3 import Error
import os


class Database:
    def __init__(self):
        if os.path.isfile(r".\database\pythonsqlite.db"):
            self.conn = self.create_connection(r".\database\pythonsqlite.db")
            return
        else:
            self.conn = self.create_connection(r".\database\pythonsqlite.db")
            sql_create_tiles_table = """ CREATE TABLE IF NOT EXISTS tiles (
                                            id integer PRIMARY KEY,
                                            name text NOT NULL,
                                            effect text NOT NULL,
                                            type text NOT NULL,
                                            North text NOT NULL,
                                            East text NOT NULL,
                                            South text NOT NULL,
                                            West text NOT NULL
                                        );"""

            sql_dev_cards_table = """ CREATE TABLE IF NOT EXISTS dev_cards (
                                            id integer PRIMARY KEY,
                                            item text NOT NULL,
                                            event_one text NOT NULL,
                                            consequence_one text NOT NULL,
                                            event_two text NOT NULL,
                                            consequence_two text NOT NULL,
                                            event_three text NOT NULL,
                                            consequence_three text NOT NULL,
                                            charges text NOT NULL
                                        );"""

            self.create_table(sql_create_tiles_table)
            self.create_table(sql_dev_cards_table)

            tile = ("Graveyard", "Bury Totem", "Outdoor", 1, 1, 0, 0)
            tile2 = ("Yard", "None", "Outdoor", 1, 1, 1, 0)
            tile3 = ("Sitting Area", "None", "Outdoor", 1, 1, 1, 0)
            tile4 = ("Yard", "None", "Outdoor", 1, 1, 1, 0)
            tile5 = ("Yard", "None", "Outdoor", 1, 1, 1, 0)
            tile6 = ("Patio", "None", "Outdoor", 1, 1, 0, 1)
            tile7 = ("Garage", "None", "Outdoor", 0, 1, 1, 0)
            tile8 = ("Garden", "Health", "Outdoor", 1, 1, 1, 0)
            tile9 = ("Bathroom", "Health", "Indoor", 0, 0, 0, 1)
            tile10 = ("Family Room", "None", "Indoor", 1, 0, 1, 1)
            tile11 = ("Kitchen", "Health", "Indoor", 1, 0, 1, 1)
            tile12 = ("Dining Room", "None", "Indoor", 1, 1, 1, 1)
            tile13 = ("Storage", "Draw", "Indoor", 0, 0, 0, 1)
            tile14 = ("Bedroom", "None", "Indoor", 0, 0, 1, 1)
            tile15 = ("Evil Temple", "Find Totem", "Indoor", 1, 0, 1, 0)
            tile16 = ("Foyer", "None", "Indoor", 0, 0, 0, 1)

            self.create_tile(tile)
            self.create_tile(tile2)
            self.create_tile(tile3)
            self.create_tile(tile4)
            self.create_tile(tile5)
            self.create_tile(tile6)
            self.create_tile(tile7)
            self.create_tile(tile8)
            self.create_tile(tile9)
            self.create_tile(tile10)
            self.create_tile(tile11)
            self.create_tile(tile12)
            self.create_tile(tile13)
            self.create_tile(tile14)
            self.create_tile(tile15)
            self.create_tile(tile16)

            dev_card = (
                "Oil",
                "Nothing",
                "None",
                "Item",
                "None",
                "Zombies",
                6,
                1,
            )
            dev_card2 = (
                "Gasoline",
                "Zombies",
                4,
                "Health",
                -1,
                "Item",
                "None",
                1,
            )
            dev_card3 = (
                "Board With Nails",
                "Item",
                "None",
                "Zombies",
                4,
                "Health",
                -1,
                "Unlimited",
            )
            dev_card4 = (
                "Machete",
                "Zombies",
                4,
                "Health",
                -1,
                "Zombies",
                6,
                "Unlimited",
            )
            dev_card5 = (
                "Grisly Femur",
                "Item",
                "None",
                "Zombies",
                5,
                "Health",
                -1,
                "Unlimited",
            )
            dev_card6 = (
                "Golf Club",
                "Health",
                -1,
                "Zombies",
                4,
                "Nothing",
                "None",
                "Unlimited",
            )
            dev_card7 = (
                "Chainsaw",
                "Zombies",
                3,
                "Nothing",
                "None",
                "Zombies",
                5,
                2,
            )
            dev_card8 = (
                "Can Of Soda",
                "Health",
                1,
                "Item",
                "None",
                "Zombies",
                4,
                1,
            )
            dev_card9 = (
                "Candle",
                "Nothing",
                "None",
                "Health",
                1,
                "Zombies",
                4,
                "Unlimited",
            )

            self.create_dev_card(dev_card)
            self.create_dev_card(dev_card2)
            self.create_dev_card(dev_card3)
            self.create_dev_card(dev_card4)
            self.create_dev_card(dev_card5)
            self.create_dev_card(dev_card6)
            self.create_dev_card(dev_card7)
            self.create_dev_card(dev_card8)
            self.create_dev_card(dev_card9)

    def create_connection(self, db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_table(self, create_table_sql):
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def create_tile(self, tile):
        sql = """ INSERT INTO tiles(name,effect,type,North,East,South,West)
              VALUES(?,?,?,?,?,?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, tile)
        self.conn.commit()

    def create_dev_card(self, tile):
        sql = """ INSERT INTO dev_cards(item,event_one,consequence_one,
            event_two,consequence_two,event_three,consequence_three,charges)
            VALUES(?,?,?,?,?,?,?,?) """
        cur = self.conn.cursor()
        cur.execute(sql, tile)
        self.conn.commit()

    def get_tiles(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM tiles")
        rows = cur.fetchall()
        return rows

    def get_dev_cards(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM dev_cards")
        rows = cur.fetchall()
        return rows

    def close_connection(self):
        self.conn.close()
