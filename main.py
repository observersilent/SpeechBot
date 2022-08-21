import logging
import time

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Application, CommandHandler, ContextTypes,
                          ConversationHandler, MessageHandler, filters)
from typing import Dict

from multiprocessing import Process
#from G2P import G2P
from Database import Database

# Включение логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Стадии опроса пользователя
CHOOSING_OPER, REPORT_REPLY, SPEACH_FORMAT, SPEACH_SPEAKER, SPEACH_TEXT, SPEACH_REPLY = range(6)
# ---------------------------------------------------------------------------------------------------

# Клавиатуры
reply_report_keyboard_commit = [
    ["Выполнить отчёт"],
    ["Отмена"],
]
markup_report_commit = ReplyKeyboardMarkup(reply_report_keyboard_commit, one_time_keyboard=True)

reply_speach_keyboard_commit = [
    ["Сгенерировать речь"],
    ["Отмена"],
]
markup_speach_commit = ReplyKeyboardMarkup(reply_speach_keyboard_commit, one_time_keyboard=True)

reply_oper_keyboard = [
    ["Генерация речи"],
    ["Запрос статистики бота"],
    ["Отмена"],
]
markup_oper = ReplyKeyboardMarkup(reply_oper_keyboard, one_time_keyboard=True)

reply_format_keyboard = [
    ["WAV"],
    ["OGG"],
    ["MP3"],
    ["Отмена"]
]
markup_format = ReplyKeyboardMarkup(reply_format_keyboard, one_time_keyboard=True)

reply_speaker_keyboard = [
    ["RUSLAN"],
    ["Артемий Лебедев"],
    ["Отмена"]
]
markup_speaker = ReplyKeyboardMarkup(reply_speaker_keyboard, one_time_keyboard=True)

reply_speach_keyboard_commit = [
    ["Сгенерировать речь"],
    ["Отмена"],
]
markup_speach_commit = ReplyKeyboardMarkup(reply_speach_keyboard_commit , one_time_keyboard=True)
# ---------------------------------------------------------------------------------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Это бот который поможет вам превратить текстовые сообщения в звуковые файлы."
        "Выберите операцию которую хотите сделать.",
        reply_markup=markup_oper,
    )

    return CHOOSING_OPER

#Выбран отчёт
async def report_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('report_choice')
    text = update.message.text
    context.user_data["type_oper"] = text
    await update.message.reply_text(f"Выбран тип операции \"{text}\".", reply_markup=markup_report_commit)

    return REPORT_REPLY

#Подтверждено что необходимо выполнить отчёт
async def report_commit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('report_commit')

    await update.message.reply_text(f"Команда подтверждена.\n"
                                    f"Операция: {context.user_data['type_oper']}\n",
                                    reply_markup=ReplyKeyboardRemove())

    context.user_data.clear()
    return ConversationHandler.END

#Выбрана генерация речи
async def speach_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('speach_choice')
    text = update.message.text
    context.user_data["type_oper"] = text
    await update.message.reply_text(f"Выбран тип операции \"{text}\".", reply_markup=markup_format)

    return SPEACH_FORMAT

#Выбран выходной формат речи
async def speach_format_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('speach_format_choice')
    text = update.message.text
    context.user_data["type_format"] = text
    await update.message.reply_text(f"Выбран формат выходного файла \"{text}\".", reply_markup=markup_speaker)

    return SPEACH_SPEAKER

# Выбран спикер
async def speach_speaker_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('speach_speaker_choice')
    text = update.message.text
    context.user_data["type_speaker"] = text
    await update.message.reply_text(f"Выбран спикер \"{text}\". \n\n"
                                    f"Введите текст который необходимо озвучить 📝")

    return SPEACH_TEXT

# Выбран текст для озвучки
async def speach_text_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('speach_text_choice')
    text = update.message.text
    context.user_data["speach_text"] = text
    await update.message.reply_text(f"Текст который необходимо озвучить: \"{text}\".", reply_markup=markup_speach_commit)

    return SPEACH_REPLY

async def speach_commit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('speach_commit')

    await update.message.reply_text(f"Команда подтверждена.\n"
                                    f"Операция: {context.user_data['type_oper']}\n"
                                    f"Выходной формат файла: {context.user_data['type_format']}\n"
                                    f"Спикер озвучки: {context.user_data['type_speaker']}\n\n"
                                    f"Текст для озвучки: {context.user_data['speach_text']}",
                                    reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END

#Отмена
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    print('вызвался done')

    await update.message.reply_text(
        f"Запрос отменен. \nДля новой попытки введите /start",
        reply_markup=ReplyKeyboardRemove(),
    )

    context.user_data.clear()
    return ConversationHandler.END

def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

    #await update.message.reply_voice(voice=open('example.ogg', 'rb'))

    #transcriptor = G2P()
    #kek = transcriptor.getTranscript(update.message.text)
    #await update.message.reply_text(str(kek))

def testFunction(g):
    database = Database()

    while True:
        print(g)
        time.sleep(20)

def main() -> None:
    # Запуск фонового процесса генерации речи
    bgProcGenSpeech = Process(target=testFunction, kwargs={"g": "kek"})
    bgProcGenSpeech.start()

    # Запуск опроса пользователей для сохранения списка запросов в БД
    application = Application.builder().token("5446887600:AAH4OwDd9GfeD0Zl7mpiQso8EI2bsREJuCY").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_OPER: [
                MessageHandler(filters.Regex("^Генерация речи$"), speach_choice),
                MessageHandler(filters.Regex("^Запрос статистики бота$"), report_choice)
            ],
            REPORT_REPLY : [
                MessageHandler(filters.Regex("^Выполнить отчёт$"), report_commit)
            ],
            SPEACH_FORMAT: [
                MessageHandler(filters.Regex("^(WAV|OGG|MP3)$"), speach_format_choice)
            ],
            SPEACH_SPEAKER: [
                MessageHandler(filters.Regex("^(RUSLAN|Артемий Лебедев)$"), speach_speaker_choice)
            ],
            SPEACH_TEXT: [
                MessageHandler(filters.TEXT & ~(filters.COMMAND | filters.Regex("^Отмена")), speach_text_choice)
            ],
            SPEACH_REPLY: [
                MessageHandler(filters.Regex("^Сгенерировать речь$"), speach_commit)
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Отмена$"), done)],
    )

    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == "__main__":
    main()