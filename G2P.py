from russian_g2p.Accentor import Accentor
from russian_g2p.Transcription import Transcription
import re

class G2P:
    def __init__(self):
        self.__accentor = Accentor(exception_for_unknown = True)
        self.__transcription = Transcription()

    #Нормализация текста
    @staticmethod
    def getTextNorm(text):
        # Приводим к нижнему регистру
        textNorm = str.lower(text)
        # Заменяем все символы кроме букв и знаков .,!? на пробелы
        textNorm = re.sub("[^А-Яа-яё,.!?+\s]", " ", text)
        # Заменяем дублированные пробелы на один пробел
        textNorm = re.sub(r'(\s)\1{1,}', r'\1', textNorm)
        # Добавляем пробелы между допустимыми символами
        textNorm = textNorm.replace(',', ' , ')
        textNorm = textNorm.replace('.', ' . ')
        textNorm = textNorm.replace('?', ' ? ')
        textNorm = textNorm.replace('!', ' ! ')
        # Заменяем дублированные пробелы на один пробел
        textNorm = re.sub(r'(\s)\1{1,}', r'\1', textNorm)
        return  textNorm

    #Функция возвращает текст в фонемном представлении
    def getTranscript(self, text):
        textNorm = self.getTextNorm(text)
        # Список слов разделённых по пробелу
        text_list = textNorm.split()

        # Проверяем знает ли ударения у всех слов
        for word in text_list:
            try:
                self.__accentor.do_accents([[word]])
            except Exception as err:
                textErr = str(err)
                if textErr.find("is unknown") != -1:
                    unknownWord = 'Не известное слово {}, поставьте знак + после ударной гласной'.format(word)
                    return unknownWord

        # Строка с поставленными ударениями на незнакомых словах подающаяся в транскриптор
        accntText = ''
        for word in text_list:
            if word not in ('.', ',', '!', '?'):
                accntText += word + '<sil>'
        # Массив фонем
        transcriptText = self.__transcription.transcribe([accntText])

        # Из фонем составляем слова
        transcript_list = []
        for i in range(len(transcriptText[0])):
            temp = '{'
            for alf in transcriptText[0][i]:
                temp += alf + ' '
            temp += '}'
            transcript_list.append(temp)

        # Ставим обратно знаки препинания
        for i in range(len(text_list)):
            if (text_list[i]) in ('.', ',', '!', '?', '…'):
                transcript_list.insert(i, text_list[i])

        rezult = ''
        for word in transcript_list:
            rezult += word

        rezult = rezult.replace(',', ', ')
        rezult = rezult.replace('.', '. ')
        rezult = rezult.replace('!', '! ')
        rezult = rezult.replace('?', '? ')
        rezult = rezult.replace('}{', '} {')

        return rezult

