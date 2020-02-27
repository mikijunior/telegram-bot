import config
import telebot
from telebot.types import InputMediaPhoto, InputMediaVideo
import os
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from random import randrange
from random import randint
from igramscraper.instagram import Instagram
import urllib.request
from igramscraper.exception import InstagramNotFoundException, InstagramException, InstagramAuthException

bot = telebot.TeleBot(config.TOKEN)

instagram = Instagram()
instaRegexp = "/(?:(?:http|https):\/\/)?(?:www\.)?(?:instagram\.com|instagr\.am)\/([A-Za-z0-9-_\.]+)/im"


@bot.message_handler(commands=['start'])
def send_welcome(message):
    sticker = open('./static/Sticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, message.from_user.first_name + ", how are you doing?")


@bot.message_handler(commands=['make_image'])
def send_image(message):
    text = message.text.replace('/make_image', '')
    if len(text) > 0:
        image_path = make_image(text)
        bot.send_photo(message.chat.id, open(image_path, 'rb'))
        os.remove(image_path)
    else:
        bot.reply_to(message, "Message too short :(")


@bot.message_handler(commands=['get_my_id'])
def get_my_id(message):
    bot.reply_to(message, message.from_user.id)


@bot.message_handler(commands=['help'])
def get_help(message):
    bot.reply_to(message, "Available commands:\n /start \n /get_my_id - return your telegram id "
                          "\n /make_image {text} - return image with your text \n /random - get random number 0 -> 100"
                          "\n /insta_photo {username} - return last 10 photo from profile")


@bot.message_handler(commands=['random'])
def get_rand(message):
    bot.reply_to(message, randint(0, 100))


@bot.message_handler(commands=['insta_photo'])
def get_instagram_profile(message):
    try:
        profile_name = message.text.replace('/insta_photo ', '')
        medias = instagram.get_medias(profile_name, 10)
        images = make_instagram_answer(medias)
        group = []
        for image in images:
            group.append(InputMediaPhoto(open(image, 'rb')))
        bot.send_media_group(message.chat.id, group)
        for image in images:
            os.remove(image)
    except InstagramNotFoundException:
        bot.reply_to(message, 'We not found this account. Make sure that your account is not private.')
    except InstagramException:
        bot.reply_to(message, 'Instagram exception.')
    except InstagramAuthException:
        bot.reply_to(message, 'Invalid credentials.')


@bot.message_handler(content_types=['text'])
def handler(message):
    bot.send_message(message.chat.id, message.text)


def make_image(text):
    font = ImageFont.truetype("./fonts/font.ttf", 72, encoding='UTF-8')
    text_with = font.getsize(text)
    img = Image.new("RGBA", (1200, 600), (randrange(0, 255), randrange(0, 255), randrange(0, 255)))
    draw = ImageDraw.Draw(img)
    max_width = 1200 - text_with[0] if 1200 - text_with[0] > 0 else 1
    draw.text((randrange(0, max_width), randrange(0, 600 - text_with[1])), text,
              (randrange(0, 255), randrange(0, 255), randrange(0, 255)),
              font)
    ImageDraw.Draw(img)
    path = "./tmp/" + text + str(randrange(0, 1000)) + ".png"
    img.save(path)
    return path


def make_instagram_answer(response):
    urls = []
    for item in response:
        account = item.owner
        path = './tmp/insta_scraper/' + str(account.username) + str(item.created_time) + '.jpg'
        urllib.request.urlretrieve(item.image_high_resolution_url, path),
        urls.append(path)

    return urls


bot.polling(none_stop=True)
