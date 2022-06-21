import telegram
from telegram.ext import Updater, MessageHandler, Filters

token = "토큰 넣기"
chat_id = "43548653"

telegram_bot = telegram.Bot(token=token)
telegram_bot.sendMessage(chat_id=chat_id, text="자동 알람 메시지")

updater = Updater(token=token, use_context=True)
dispather = updater.dispatcher
updater.start_polling()

def handler(updata, context):
    user_text = updata.message.text
    if user_text == "1":
        telegram_bot.send_message(chat_id=chat_id, text="1이 입력되었습니다")
    elif user_text == "2":
        telegram_bot.send_message(chat_id=chat_id, text="2가 입력되었습니다")

echo_handler = MessageHandler(Filters.text, handler)