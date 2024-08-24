import asyncio
import io
import json
import logging
import os
import sys
from typing import Iterable

import google.generativeai as genai2
import gspread
import PIL.Image
from subprocess import Popen
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, Poll
from attrs import define

from aigen import GenAI


@define
class MessageTransformed:
    first_name: str
    date: str

    def __init__(self, message_aiogrm: Message) -> None:
        self.date = message_aiogrm.date.strftime('%d.%m.%Y %H:%M:%S') or ""
        self.first_name = message_aiogrm.from_user.first_name

    def __dir__(self) -> Iterable[str]:
        return [
            'first name: ',
            self.first_name,
            'date: ',
            self.date,
        ]


class BotAI(Bot):

    def __init__(self,
                 token: str,
                 session=None,
                 default=None,
                 **kwargs) -> None:
        self.genai = GenAI("models/gemini-1.5-flash")
        self.chat = self.genai.start_chat()
        super().__init__(token, session, default, **kwargs)


TOKEN = os.environ["BOT_TOKEN"]

gc = gspread.service_account_from_dict(
    json.loads(str(os.environ["credentials"])))
dp = Dispatcher()

sh = gc.open_by_key('1ToJydqqVwS5IQQcmilMFDCsSElON-WSPYYUx_50rVdw')


@dp.message(F.text)
async def handler_text(message: Message, bot: BotAI) -> None:
    try:
        worksheet = sh.worksheet(str(message.from_user.id))
    except gspread.WorksheetNotFound:
        worksheet = sh.add_worksheet(str(message.from_user.id), 10000, 6)
        worksheet.update_acell('F1', 1)

    message_transformed = MessageTransformed(message)
    i = int(worksheet.get('F1')[0][0])
    worksheet.update_acell('F1', i + 1)
    worksheet.update([[
        message.message_id, message_transformed.date, "Text", message.text,
        json.loads(
            bot.chat.send_message([
                *dir(message_transformed), "text: ", message.text
            ]).text)['toxicity']
    ]], f'A{i}:E{i}')
    # await message.reply(
    #     bot.chat.send_message(
    #         [*dir(MessageTransformed(message)), "text: ", message.text]).text)


@dp.message(F.photo)
async def handler_photo(message: Message, bot: BotAI) -> None:
    try:
        worksheet = sh.worksheet(str(message.from_user.id))
    except gspread.WorksheetNotFound:
        worksheet = sh.add_worksheet(str(message.from_user.id), 10000, 6)
        worksheet.update_acell('F1', 1)

    message_transformed = MessageTransformed(message)
    i = int(worksheet.get('F1')[0][0])
    worksheet.update_acell('F1', i + 1)

    file_photo: io.BytesIO = await bot.download(message.photo[-1])
    message_caption = message.caption if message.caption else ''

    worksheet.update([[
        message.message_id, message_transformed.date, "Photo", message_caption,
        json.loads(
            bot.chat.send_message([
                *dir(message_transformed), "caption: ", message_caption,
                "photo: ",
                PIL.Image.open(file_photo)
            ]).text)['toxicity']
    ]], f'A{i}:E{i}')
    # await message.reply(
    #     bot.chat.send_message([
    #         *dir(message_transformed), "caption: ", message_caption,
    #         "photo: ",
    #         PIL.Image.open(file_photo)
    #     ]).text)


@dp.message((F.sticker) & ~((F.sticker.is_animated) | (F.sticker.is_video)))
async def handler_sticker(message: Message, bot: BotAI) -> None:
    try:
        worksheet = sh.worksheet(str(message.from_user.id))
    except gspread.WorksheetNotFound:
        worksheet = sh.add_worksheet(str(message.from_user.id), 10000, 6)
        worksheet.update_acell('F1', 1)

    message_transformed = MessageTransformed(message)
    i = int(worksheet.get('F1')[0][0])
    worksheet.update_acell('F1', i + 1)

    file_photo: io.BytesIO = await bot.download(message.sticker)

    worksheet.update([[
        message.message_id, message_transformed.date, "Sticker",
        message.sticker.emoji,
        json.loads(
            bot.chat.send_message([
                *dir(message_transformed), "emoji: ", message.sticker.emoji,
                "sticker: ",
                PIL.Image.open(file_photo)
            ]).text)['toxicity']
    ]], f'A{i}:E{i}')
    # await message.reply(
    #     bot.chat.send_message([
    #         *dir(message_transformed), "emoji: ", message.sticker.emoji,
    #         "sticker: ",
    #         PIL.Image.open(file_photo)
    #     ]).text)


@dp.message(F.animation)
async def handler_animation(message: Message, bot: BotAI) -> None:
    try:
        worksheet = sh.worksheet(str(message.from_user.id))
    except gspread.WorksheetNotFound:
        worksheet = sh.add_worksheet(str(message.from_user.id), 10000, 6)
        worksheet.update_acell('F1', 1)

    message_transformed = MessageTransformed(message)
    i = int(worksheet.get('F1')[0][0])
    worksheet.update_acell('F1', i + 1)

    await bot.download(message.animation, "video2.mp4")
    video_file = genai2.upload_file(path="video2.mp4")
    await asyncio.sleep(5)

    worksheet.update([[
        message.message_id, message_transformed.date, "Gif", "",
        json.loads(
            bot.chat.send_message([
                *dir(message_transformed), "gif: ", video_file
            ]).text)['toxicity']
    ]], f'A{i}:E{i}')
    # await message.reply(
    #     bot.chat.send_message(
    #         [*dir(MessageTransformed(message)), "gif: ", video_file]).text)


@dp.message(F.video)
async def handler_video(message: Message, bot: BotAI) -> None:
    try:
        worksheet = sh.worksheet(str(message.from_user.id))
    except gspread.WorksheetNotFound:
        worksheet = sh.add_worksheet(str(message.from_user.id), 10000, 6)
        worksheet.update_acell('F1', 1)

    message_transformed = MessageTransformed(message)
    i = int(worksheet.get('F1')[0][0])
    worksheet.update_acell('F1', i + 1)

    await bot.download(message.video, "video3.mp4")
    video_file = genai2.upload_file(path="video3.mp4")
    message_caption = message.caption if message.caption else ''
    await asyncio.sleep(5)

    worksheet.update([[
        message.message_id, message_transformed.date, "Video", message_caption,
        json.loads(
            bot.chat.send_message([
                *dir(message_transformed), "caption: ", message_caption,
                "video: ", video_file
            ]).text)['toxicity']
    ]], f'A{i}:E{i}')

    # await message.reply(
    #     bot.chat.send_message([
    #         *dir(MessageTransformed(message)), "caption: ", message_caption,
    #         "video: ", video_file
    #     ]).text)


# TODO: make poll
@dp.message(F.poll)
async def handler_poll(message: Message, bot: BotAI) -> None:
    try:
        worksheet = sh.worksheet(str(message.from_user.id))
    except gspread.WorksheetNotFound:
        worksheet = sh.add_worksheet(str(message.from_user.id), 10000, 6)
        worksheet.update_acell('F1', 1)

    message_transformed = MessageTransformed(message)
    i = int(worksheet.get('F1')[0][0])
    worksheet.update_acell('F1', i + 1)

    poll: Poll = message.poll

    worksheet.update([[
        message.message_id, message_transformed.date, "Poll", poll.question,
        json.loads(
            bot.chat.send_message([
                *dir(message_transformed), "poll question: ", poll.question,
                "poll options: ", *[option.text for option in poll.options]
            ]).text)['toxicity']
    ]], f'A{i}:E{i}')

    # await message.reply(
    #     bot.chat.send_message([
    #         *dir(message_transformed), "poll question: ",
    #         poll.question, "poll options: ",
    #         *[option.text for option in poll.options]
    #     ]).text)


# @dp.message(F.document)
async def handler_document(message: Message, bot: BotAI) -> None:
    file_document: io.BytesIO = await bot.download(message.document)
    message_caption = message.caption if message.caption else ''
    await message.reply(
        bot.chat.send_message([
            *dir(MessageTransformed(message)), "caption: ", message_caption,
            "document: ", {
                "mime_type": message.document.mime_type,
                "data": file_document.read()
            }
        ]).text)


# @dp.message(F.voice)
async def handler_voice(message: Message, bot: BotAI) -> None:
    file_voice: io.BytesIO = await bot.download(message.voice)

    await message.reply(
        bot.chat.send_message([
            *dir(MessageTransformed(message)), "voice: ", {
                "mime_type": message.voice.mime_type,
                "data": file_voice.read()
            }
        ]).text)


@dp.message((F.sticker) & (F.sticker.is_video))
async def handler_stikcer_video(message: Message, bot: BotAI) -> None:
    try:
        worksheet = sh.worksheet(str(message.from_user.id))
    except gspread.WorksheetNotFound:
        worksheet = sh.add_worksheet(str(message.from_user.id), 10000, 6)
        worksheet.update_acell('F1', 1)

    message_transformed = MessageTransformed(message)
    i = int(worksheet.get('F1')[0][0])
    worksheet.update_acell('F1', i + 1)

    await bot.download(message.sticker, "video.mp4")
    video_file = genai2.upload_file(path="video.mp4")
    await asyncio.sleep(2)

    worksheet.update([[
        message.message_id, message_transformed.date, "Sticker",
        message.sticker.emoji,
        json.loads(
            bot.chat.send_message([
                *dir(message_transformed),
                message.date.strftime('%d.%m.%Y %H:%M:%S'), "emoji: ",
                message.sticker.emoji, "video sticker: ", video_file
            ]).text)['toxicity']
    ]], f'A{i}:E{i}')

    # await message.reply(
    #     bot.chat.send_message([
    #         *dir(message_transformed),
    #         message.date.strftime('%d.%m.%Y %H:%M:%S'), "emoji: ",
    #         message.sticker.emoji, "video sticker: ", video_file
    #     ]).text)


async def main() -> None:
    bot = BotAI(token=TOKEN)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    Popen(["python", "keep_alive.py"])
    asyncio.run(main())
