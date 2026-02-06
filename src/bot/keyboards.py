from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config.logger_config import logger
from downloader.downloader import Downloader

async def streams_kb(video:Downloader) -> InlineKeyboardMarkup | None:
    """
    Строит инлайн-клавиатуру для потоков видео
    
    :param video: Объект видео
    :type video: Downloader
    :return: инлайн клавиатура
    :rtype: InlineKeyboardMarkup | None
    """
    # Получаем информацию о потоках
    streams_info = await video.get_streams_info()
    logger.debug(streams_info)

    # Строим клавиатуру
    if streams_info != None:
        builder = InlineKeyboardBuilder()
        for resolution, data in streams_info.items():
            builder.row(
                InlineKeyboardButton(
                    text=resolution,
                    callback_data=data
                )
            )
        builder.adjust(1)
        return builder.as_markup()
    else:
        return None