from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from pytubefix import AsyncYouTube
from pytubefix.exceptions import VideoUnavailable, RegexMatchError

from utils.string_utils import format_time_from_seconds
from config.logger_config import logger
from config.fsm_config import UserStates
from localization.messages_localization import (invalid_link_message,
                                                video_preview_message)
from bot.keyboards import streams_kb

# Устанавливаем роутер
user_router = Router()

# Обработка получения ссылки на видео
@user_router.message(UserStates.link_waiting, F.text != None)
async def handle_link(message: Message, state: FSMContext):
    try:
        yt = AsyncYouTube(url=message.text, use_oauth=True, allow_oauth_cache=True)

        # Получаем метаданные видео
        video_duration = format_time_from_seconds(await yt.length())
        answer = video_preview_message.format(await yt.title(),
                                              await yt.author(),
                                              video_duration)
        # Получаем доступные потоки видео
        streams = await yt.streams()
        await message.answer(text=answer, reply_markup=streams_kb(streams))
    except (VideoUnavailable, RegexMatchError) as e:
        await message.answer(invalid_link_message)
        logger.warning(e)