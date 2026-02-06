from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from pytubefix import StreamQuery, Stream

from utils.yt_utils import get_resolution_dict
from config.logger_config import logger

def streams_kb(streams:StreamQuery):
    builder = InlineKeyboardBuilder()
    resolutions = get_resolution_dict(streams)
    logger.debug(resolutions)

    for resolution, itag in resolutions.items():
        builder.row(
            InlineKeyboardButton(
                text=resolution,
                callback_data=itag
            )
        )
    builder.adjust(1)
    return builder.as_markup()