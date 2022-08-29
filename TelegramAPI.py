import asyncio
from telegram import Bot

class TelegramAPI:
    _token = '5446887600:AAH4OwDd9GfeD0Zl7mpiQso8EI2bsREJuCY'
    def __init__(self):
        self.bot = Bot(token=self._token)

    def sendMessage(self, text):

        async def sendMessageAsync():
            async with self.bot:
                await self.bot.sendMessage(chat_id=370018182, text = text)

        loop = asyncio.get_event_loop()
        coroutine = sendMessageAsync()
        loop.run_until_complete(coroutine)
