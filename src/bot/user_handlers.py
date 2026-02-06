from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config.fsm_config import UserStates
from bot.keyboards import streams_kb
from downloader.downloader import Downloader
from localization.messages_localization import video_preview_message
from localization.errors_localization import (no_info_err, 
                                              invalid_link_err,
                                              no_streams_err)


# Устанавливаем роутер
user_router = Router()

# Обработка получения ссылки на видео
@user_router.message(UserStates.link_waiting, F.text != None)
async def handle_link(message: Message, state: FSMContext) -> None:
    video = Downloader(url=message.text) # type: ignore
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

