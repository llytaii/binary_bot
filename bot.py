import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, 
    text="This bot translates messages into binary using utf-8")

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def is_binary(s: str):
    for c in s:
        if c != '0' and c != '1':
            return False
    return True

def translate(update: Update, context: CallbackContext) -> None:
    s = update.message.text
    if(is_binary(s)):
        s = text_from_bits(s)
    else:
        s = text_to_bits(s)
    update.message.reply_text(s)


def main() -> None:
    with open('token.txt') as f:
        token = f.read().strip()

    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, translate))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()