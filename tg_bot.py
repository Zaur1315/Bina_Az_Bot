import asyncio
import json
from main import check_new_post
from aiogram import Bot, Dispatcher, executor, types
from config import token, user_id
from aiogram.dispatcher.filters import Text



bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start(message : types.Message):
    start_buttons = ["Все объявления", "Последние 5 объявлений", "Свежие объяления"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Вас приветствует Бот-Маклер.Дальше вам будет удобнее пользоваться вспомогательными кнопками.', reply_markup=keyboard)

@dp.message_handler(Text(equals='Все объявления'))
async def get_all_news(message: types.Message):
    with open('new_dict.json',encoding='utf-8') as file:
        new_dict = json.load(file)

    for k, v in sorted(new_dict.items()):
        news = f'<b>{v["article_title"]}</b>\n'\
               f'{v["article_desc"]}\n'\
               f'{v["article_price"]}\n'\
               f'{v["article_url"]}'


        await  message.answer(news)

@dp.message_handler(Text(equals='Последние 5 объявлений'))
async def get_last_five_post(message: types.Message):
    with open('new_dict.json',encoding='utf-8') as file:
        new_dict = json.load(file)

    for k, v in sorted(new_dict.items())[-5:]:
        news = f'<b>{v["article_title"]}</b>\n'\
               f'{v["article_desc"]}\n'\
               f'{v["article_price"]}\n'\
               f'{v["article_url"]}'
        await message.answer(news)

@dp.message_handler(Text(equals='Свежие объяления'))
async def fresh_post(message: types.Message):
    await message.answer('Поиск объявлений...')
    fresh_post = check_new_post()
    if len(fresh_post) >= 1:
        for k, v in fresh_post.items():
            news = f'<b>{v["article_title"]}</b>\n'\
                   f'{v["article_desc"]}\n' \
                   f'{v["article_price"]}\n'\
                   f'{v["article_url"]}'
            await  message.answer(news)
    else:
        await message.answer('Пока нет новых объявлений')

async def news_every_minute():
    while True:
        fresh_post = check_new_post()
        if len(fresh_post) >= 1:
            for k, v in fresh_post.items():
                news = f'<b>{v["article_title"]}</b>\n'\
                       f'{v["article_desc"]}\n' \
                       f'{v["article_price"]}\n'\
                       f'{v["article_url"]}'
                await bot.send_message(user_id, news, disable_notification=True)
                # await bot.send_message(user_id2, news, disable_notification=True)


        await asyncio.sleep(40)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)
