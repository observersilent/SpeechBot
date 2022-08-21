FROM python:3.7.5-slim

COPY . ./bot
WORKDIR ./bot

RUN apt-get update && apt-get install -y gcc && apt-get install -y g++

# Установка API Telegram
RUN pip install --no-index -f ./wheels/telegramBotApi -r requirements.txt

# Установка russianG2P
RUN pip install --no-index -f ./wheels/russianG2P -r requirements2.txt

CMD [ "python" , "main.py" ]
