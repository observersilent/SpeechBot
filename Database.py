import os
import sqlite3
from contextlib import closing

class Database:
    def __init__(self):
        self.__db = r'database.sqlite'
        #Если БД отсутствует, создаём
        if not os.path.isfile(self.__db):
            with closing(sqlite3.connect(self.__db)) as conn:
                cur = conn.cursor()

                cur.execute("""
                            CREATE TABLE IF NOT EXISTS user_role (
                                id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                                name VARCHAR (200) NOT NULL UNIQUE);                 
                """)
                conn.commit()
                data = [(1, 'Админ'), (2, 'Пользователь')]
                cur.executemany("INSERT INTO user_role VALUES(?, ?);", data)
                conn.commit()
                #----------------------------------------------------------------------------------------
                cur.execute("""
                            CREATE TABLE IF NOT EXISTS type_query (
                                id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                                name VARCHAR (200) UNIQUE NOT NULL);
                """)
                conn.commit()
                data = [(1, 'Генерация речи'), (2, 'Запрос статистики бота')]
                cur.executemany("INSERT INTO type_query VALUES(?, ?);", data)
                conn.commit()
                # ----------------------------------------------------------------------------------------
                cur.execute("""
                            CREATE TABLE IF NOT EXISTS status_query (
                                id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                                name VARCHAR (200) UNIQUE NOT NULL);
                """)
                conn.commit()
                data = [(1, 'Выполнен'), (2, 'Не выполнен'), (3, 'Ошибка')]
                cur.executemany("INSERT INTO status_query VALUES(?, ?);", data)
                conn.commit()
                # ----------------------------------------------------------------------------------------
                cur.execute("""
                            CREATE TABLE IF NOT EXISTS speaker_list (
                                id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                                name VARCHAR UNIQUE NOT NULL);
                """)
                conn.commit()
                data = [(1, 'RUSLAN'), (2, 'Артемий Лебедев')]
                cur.executemany("INSERT INTO speaker_list VALUES(?, ?);", data)
                conn.commit()
                # ----------------------------------------------------------------------------------------
                cur.execute("""
                            CREATE TABLE IF NOT EXISTS format_list (
                                id INTEGER PRIMARY KEY NOT NULL UNIQUE,
                                name VARCHAR UNIQUE NOT NULL);
                """)
                conn.commit()
                data = [(1, 'WAV'), (2, 'OGG'), (3, 'MP3')]
                cur.executemany("INSERT INTO format_list VALUES(?, ?);", data)
                conn.commit()
                # ----------------------------------------------------------------------------------------
                cur.execute("""
                            CREATE TABLE IF NOT EXISTS [query] (
                                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                date_begin DATETIME NOT NULL,
                                date_end DATETIME,
                                chat_id VARCHAR NOT NULL,
                                id_user_role INTEGER REFERENCES user_role (id) NOT NULL,
                                id_type_query INTEGER REFERENCES type_query (id) NOT NULL,
                                id_format_list INTEGER REFERENCES format_list (id),
                                id_speaker_list INTEGER REFERENCES speaker_list (id),
                                speach_text VARCHAR (2000),
                                speach_file BLOB,
                                id_status INTEGER REFERENCES status_query (id) NOT NULL,
                                error_text VARCHAR (4000));
                """)
                conn.commit()