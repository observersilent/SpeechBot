import os
import sqlite3
from contextlib import closing

class Database:
    def __init__(self):
        self.__db = r'database.sqlite'
        self.__admin = [370018182]

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
                                id_format INTEGER REFERENCES format_list (id),
                                id_speaker INTEGER REFERENCES speaker_list (id),
                                speach_text VARCHAR (2000),
                                speach_file BLOB,
                                id_status INTEGER REFERENCES status_query (id) NOT NULL,
                                error_text VARCHAR (4000));
                """)
                conn.commit()

        self.__dictRole = self.getUserRoleDict()
        self.__dictTypeQuery = self.getTypeQueryDict()
        self.__dictStatusQuery = self.getStatusQueryDict()
        self.__dictSpeaker = self.getSpeakerDict()
        self.__dictFormat = self.getFormatDict()

    #функция возвращает словарь ролей пользователя в виде роль : ключ
    def getUserRoleDict(self):
        with closing(sqlite3.connect(self.__db)) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM user_role")
            listUserRole = cur.fetchall()
            dictUserRole = {role[1] : role[0] for role in listUserRole}
            return dictUserRole

    #функция возвращает словарь типов запросов в виде тип : ключ
    def getTypeQueryDict(self):
        with closing(sqlite3.connect(self.__db)) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM type_query")
            listTypeQuery = cur.fetchall()
            dictTypeQuery = {type[1] : type[0] for type in listTypeQuery}
            return dictTypeQuery

    #функция возвращает словарь статус запросов в виде статус : ключ
    def getStatusQueryDict(self):
        with closing(sqlite3.connect(self.__db)) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM status_query")
            listStatusQuery = cur.fetchall()
            dictStatusQuery = {status[1] : status[0] for status in listStatusQuery}
            return dictStatusQuery

    #функция возвращает словарь спикеров в виде спикер : ключ
    def getSpeakerDict(self):
        with closing(sqlite3.connect(self.__db)) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM speaker_list")
            listSpeaker = cur.fetchall()
            dictSpeaker = {speaker[1] : speaker[0] for speaker in listSpeaker}
            return dictSpeaker

    #функция возвращает словарь форматов выходных звуковых файлов в виде формат : ключ
    def getFormatDict(self):
        with closing(sqlite3.connect(self.__db)) as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM format_list")
            listFormat = cur.fetchall()
            dictFormat = {format[1] : format[0] for format in listFormat}
            return dictFormat


    def getUserRoleId(self, from_id):
        if from_id in self.__admin:
            return self.__dictRole['Админ']
        else:
            return self.__dictRole['Пользователь']

    def getTypeQueryId(self, typequery):
        return self.__dictTypeQuery[typequery]

    def getStatusQueryId(self, status):
        return self.__dictStatusQuery[status]

    def getSpeakerId(self, speaker):
        return self.__dictSpeaker[speaker]

    def getFormatId(self, format):
        return self.__dictFormat[format]


    def insertQueryReport(self, id_chat, id_user_role, id_type_query):
        try:
            #gg = 1.0 / 0
            with closing(sqlite3.connect(self.__db)) as conn:
                sql = (f"INSERT INTO [query] (date_begin, chat_id, id_user_role, id_type_query, id_status)"
                            f"VALUES (datetime('now'), "
                                  f"{id_chat}, "
                                   f"{id_user_role}, "
                                 f"{id_type_query}, "
                                 f"{self.getStatusQueryDict()['Не выполнен']});")
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()

        except Exception as ex:
            return ex
        else:
            return None

    def insertQuerySpeach(self, id_chat, id_user_role, id_type_query, id_format, id_speaker, text):
        try:
            with closing(sqlite3.connect(self.__db)) as conn:
                sql = (f"INSERT INTO [query] (date_begin, chat_id, id_user_role, id_type_query, "
                                            f"id_format, id_speaker, speach_text, id_status)"
                            f"VALUES (datetime('now'), "
                                  f"{id_chat}, "
                                  f"{id_user_role}, "
                                  f"{id_type_query}, "
                                  f"{id_format}, "
                                  f"{id_speaker}, "
                                  f"'{text}', "
                                  f"{self.__dictStatusQuery['Не выполнен']});")
                cur = conn.cursor()
                cur.execute(sql)
                conn.commit()

        except Exception as ex:
            return ex
        else:
            return None

    def getUndoneQuerySpeach(self):
        with closing(sqlite3.connect(self.__db)) as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT id, chat_id, id_format, id_speaker, speach_text "
                          f"FROM [query] "
                         f"WHERE id_type_query = {self.getTypeQueryId('Генерация речи')} "
                           f"AND id_status = {self.getStatusQueryId('Не выполнен')}")
            listQuerySpeach = cur.fetchall()
            return listQuerySpeach

    def processError(self, errList, bot):
        for err in errList:
            type = err[0]
            if type == 'Генерация речи':
                data = err[1]
                message = err[2]

                with closing(sqlite3.connect(self.__db)) as conn:
                    cur = conn.cursor()
                    cur.execute(f"UPDATE [query] SET date_end = datetime(\'now\'), "
                                                   f"id_status = {self.getStatusQueryId('Ошибка')}, "
                                                   f"error_text = '{message}' "
                              f"WHERE id = {data[0]}" )
                    conn.commit()

                bot.sendMessage('Тест')