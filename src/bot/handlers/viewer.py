from io import BytesIO
from tempfile import TemporaryFile

import PIL.Image
from aiogram import Router
from aiogram import F
from aiogram.enums import ContentType
from aiogram.types import Message

from types.bot import BotAI
from types.data import QueueDataText, QueueDataPhoto, QueueDataVideo

viewer_router = Router()


@viewer_router.message(F.text)
async def viewer_text_handler(message: Message, bot: BotAI):
    bot.queue.put(QueueDataText(
        ContentType.TEXT,
        message.from_user,
        message.date,
        message.text
    ))


@viewer_router.message(F.photo)
async def viewer_photo_handler(message: Message, bot: BotAI):
    bytes_io = BytesIO()
    await bot.download(message.photo[-1], bytes_io)
    bot.queue.put(QueueDataPhoto(
        message.from_user,
        message.date,
        message.caption,
        PIL.Image.open(bytes_io)
    ))


@viewer_router.message(F.sticker & ~(F.sticker.is_animated | F.sticker.is_video))
async def viewer_sticker_handler(message: Message, bot: BotAI):
    bytes_io = BytesIO()
    await bot.download(message.sticker, bytes_io)
    bot.queue.put(QueueDataPhoto(
        message.from_user,
        message.date,
        message.caption,
        PIL.Image.open(bytes_io)
    ))


@viewer_router.message(F.animation)
async def viewer_animation_handler(message: Message, bot: BotAI):
    temp = TemporaryFile('w+b')
    await bot.download(message.sticker, temp.name)
    bot.queue.put(QueueDataVideo(
        message.from_user,
        message.date,
        message.caption,
        temp
    ))
