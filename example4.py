import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, helpers
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define constants that will allow us to reuse the deep-linking parameters.
CHECK_THIS_OUT = "check-this-out"
USING_ENTITIES = "using-entities-here"
USING_KEYBOARD = "using-keyboard-here"
SO_COOL = "so-cool"

# Callback data to pass in 3rd level deep-linking
KEYBOARD_CALLBACKDATA = "keyboard-callback-data"

#Отправить ссылку перейдя по которой можно выбрать в какую группу добавить бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a deep-linked URL when the command /start is issued."""
    bot = context.bot
    url = helpers.create_deep_linked_url(bot.username, CHECK_THIS_OUT, group=True)
    text = "Feel free to tell your friends about it:\n\n" + url
    await update.message.reply_text(text)

#Открыть предложение запустить бот при помощи кнопочки в приватном канале - сообщение в добавленной группе
async def deep_linked_level_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reached through the CHECK_THIS_OUT payload"""
    bot = context.bot
    url = helpers.create_deep_linked_url(bot.username, SO_COOL)
    text = (
        "Awesome, you just accessed hidden functionality! "
        "Now let's get back to the private chat."
    )
    keyboard = InlineKeyboardMarkup.from_button(
        InlineKeyboardButton(text="Continue here!", url=url)
    )
    await update.message.reply_text(text, reply_markup=keyboard)


async def deep_linked_level_2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reached through the SO_COOL payload"""
    bot = context.bot
    url = helpers.create_deep_linked_url(bot.username, USING_ENTITIES)
    text = f'You can also mask the deep-linked URLs as links: <a href="{url}">▶️ CLICK HERE</a>.'
    await update.message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


async def deep_linked_level_3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reached through the USING_ENTITIES payload"""
    await update.message.reply_text(
        "It is also possible to make deep-linking using InlineKeyboardButtons.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Like this!", callback_data=KEYBOARD_CALLBACKDATA)]]
        ),
    )


async def deep_link_level_3_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Answers CallbackQuery with deeplinking url."""
    bot = context.bot
    url = helpers.create_deep_linked_url(bot.username, USING_KEYBOARD)
    await update.callback_query.answer(url=url)


async def deep_linked_level_4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Reached through the USING_KEYBOARD payload"""
    payload = context.args
    await update.message.reply_text(
        f"Congratulations! This is as deep as it gets 👏🏻\n\nThe payload was: {payload}"
    )


def main() -> None:
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5446887600:AAH4OwDd9GfeD0Zl7mpiQso8EI2bsREJuCY").build()

    # Register a deep-linking handler
    application.add_handler(
        CommandHandler("start", deep_linked_level_1, filters.Regex(CHECK_THIS_OUT))
    )

    # This one works with a textual link instead of an URL
    application.add_handler(CommandHandler("start", deep_linked_level_2, filters.Regex(SO_COOL)))

    # We can also pass on the deep-linking payload
    application.add_handler(
        CommandHandler("start", deep_linked_level_3, filters.Regex(USING_ENTITIES))
    )

    # Possible with inline keyboard buttons as well
    application.add_handler(
        CommandHandler("start", deep_linked_level_4, filters.Regex(USING_KEYBOARD))
    )

    # register callback handler for inline keyboard button
    application.add_handler(
        CallbackQueryHandler(deep_link_level_3_callback, pattern=KEYBOARD_CALLBACKDATA)
    )

    # Make sure the deep-linking handlers occur *before* the normal /start handler.
    application.add_handler(CommandHandler("start", start))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()