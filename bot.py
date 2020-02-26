import config
import telebot
import os
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from random import randrange
from random import randint


bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    sticker = open('./static/Sticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.reply_to(message, message.from_user.username + ", how are you doing?")


@bot.message_handler(commands=['makeImage'])
def send_image(message):
    text = message.text.replace('/makeImage', '')
    if len(text) > 0:
        image_path = make_image(text)
        bot.send_photo(message.chat.id, open(image_path, 'rb'))
        os.remove(image_path)
    else:
        bot.reply_to(message, "Message too short :(")


@bot.message_handler(commands=['getMyId'])
def get_my_id(message):
    bot.reply_to(message, message.from_user.id)


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.reply_to(message, "Available commands:\n /start \n /getMyId - return your telegram id "
                          "\n /makeImage {text} - return image with your text \n /random - get random number 0 -> 100")


@bot.message_handler(commands=['random'])
def get_rand(message):
    bot.reply_to(message, randint(0, 100))


@bot.message_handler(content_types=['text'])
def handler(message):
    bot.send_message(message.chat.id, message.text)


def make_image(text):
    font = ImageFont.truetype("./fonts/Raleway-Italic.ttf", 72, encoding='unic')
    text_with = font.getsize(text)
    img = Image.new("RGBA", (1200, 600), (randrange(0, 255), randrange(0, 255), randrange(0, 255)))
    draw = ImageDraw.Draw(img)
    draw.text((randrange(0, 1200 - text_with[0]), randrange(0, 600 - text_with[1])), text,
              (randrange(0, 255), randrange(0, 255), randrange(0, 255)),
              font)
    ImageDraw.Draw(img)
    path = "./tmp/" + text + str(randrange(0, 1000)) + ".png"
    img.save(path)
    return path


bot.polling(none_stop=True)
