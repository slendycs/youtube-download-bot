from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config.fsm_config import UserStates
from localization.messages_localization import *

# Устанавливаем роутер
command_router = Router()

@command_router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text=start_message)
    await state.set_state(UserStates.link_waiting)