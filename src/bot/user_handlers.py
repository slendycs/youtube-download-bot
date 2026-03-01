from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config.logger_config import logger
from config.fsm_config import UserStates
from bot.keyboards import streams_kb
from downloader.downloader import Downloader
from utils.string_utils import serialize_request
from localization.messages_localization import (video_preview_message,
                                                download_started_message,
                                                download_finished_message)
from localization.errors_localization import (no_info_err, 
                                              invalid_link_err,
                                              no_streams_err)


# Устанавливаем роутер
user_router = Router()

# Обработка получения ссылки на видео
@user_router.message(UserStates.link_waiting, F.text != None)
async def handle_link(message:Message, state:FSMContext) -> None:
    video = Downloader(url=message.text)
    if video.video == None:
        await message.answer(invalid_link_err)
        return
    
    # Получаем информацию о видео
    video_info = await video.get_video_info()
    if video_info == None:
        await message.answer(no_info_err)
        return
    
    # Форматируем сообщение с информацией о видео
    answer = video_preview_message.format(video_info['title'],
                                          video_info['author'],
                                          video_info['duration'])
    # Строим клавиатуру
    keyboard = await streams_kb(video)
    if keyboard == None:
        await message.answer(no_streams_err)
          
    # Отправляем информацию о видео
    await message.answer(text=answer, reply_markup=keyboard)
    await state.set_state(UserStates.resolution_choice)


# Обработка результата нажатия кнопки выбора разрешения
@user_router.callback_query(UserStates.resolution_choice, F.data.startswith('itag_'))
async def handle_resolution_callback(call:CallbackQuery, state:FSMContext) -> None:
    # Получаем запрос от нажатия кнопки
    await call.answer()
    request = call.data
    if request == None:
        logger.error("Failed to retrieve information after pressing the button")
        return
    
    # Уведомляем о начале загрузки
    await call.bot.edit_message_text(text=download_started_message,
                                     chat_id=call.from_user.id,
                                     message_id=call.message.message_id,
                                     reply_markup=None)

    # Получаем видео по эти данным
    video_data = serialize_request(request)
    video = Downloader(video_id=video_data.get('video_id'))

    # Скачиваем видео
    download_path = await video.download(int(video_data.get('itag')))

    # Проверяем успешность загрузки
    if download_path != None:
        logger.info(f'Video was downloaded: {download_path}')
        await call.bot.edit_message_text(text=download_finished_message,
                                         chat_id=call.from_user.id,
                                         message_id=call.message.message_id,
                                         reply_markup=None)
        await state.set_state(UserStates.link_waiting)
    else:
        pass