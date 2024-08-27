from tempfile import TemporaryFile
from datetime import datetime

from PIL.Image import Image
from aiogram.enums import ContentType
from aiogram.types import User

from attrs import define


@define
class QueueData:
    type: ContentType
    user: User
    date: datetime


@define
class QueueDataText(QueueData):
    text: str


@define
class QueueDataPhoto(QueueData):
    caption: str
    image: Image


@define
class QueueDataVideo(QueueData):
    caption: str
    video: TemporaryFile
