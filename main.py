import os
import qrcode
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Telegram bot token'ını ayarla
TOKEN = os.environ['TG_TOKEN']
updater = Updater(token=TOKEN, use_context=True)

# QR kodunu oluşturma fonksiyonu
def create_qr_code(text):
    # QR kodu oluştur
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(text)
    qr.make(fit=True)

    # QR kodu resmine dönüştür
    img = qr.make_image(fill_color="black", back_color="white")
    return img

# /start komutunu işle
def start(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Merhaba! Benim adım ChatGPT. Ben bir yapay zeka botuyum. Sana yardımcı olabileceğim herhangi bir konuda bana bir mesaj gönderin.")

# /qr komutunu işle
def qr(update: Update, context: CallbackContext) -> None:
    text = context.args[0]
    img = create_qr_code(text)

    # QR kodu resmini gönder
    img_file = "qr_code.png"
    img.save(img_file)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(img_file, 'rb'))

# Gelen mesajları işle
def echo(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text.startswith("/qr "):
        qr_text = text[4:]
        img = create_qr_code(qr_text)

        # QR kodu resmini gönder
        img_file = "qr_code.png"
        img.save(img_file)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(img_file, 'rb'))
    else:
        response = openai.Completion.create(
            engine="davinci",
            prompt=text,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5
        )
        context.bot.send_message(chat_id=update.effective_chat.id, text=response.choices[0].text)

# Komut ve mesaj işleyicilerini kaydet
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('qr', qr))
updater.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# Botu çalıştır
updater.start_polling()