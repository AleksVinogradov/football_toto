from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message

from keyboards.menu_keyboards import menu_cd, categories_keyboard, leagues_keyboard, \
    matches_keyboard, bet_keyboard
from loader import dp
from utils.db_commands import get_match


# хендлер на команду /menu
@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    await list_categories(message)


# функция, которая выдает категории
async def list_categories(message: Union[CallbackQuery, Message], **kwargs):
    markup = await categories_keyboard()  # формируем клавиатуру
    if isinstance(message, Message):  # если message - отправляем новое сообщение
        await message.answer("Сделайте, пожалуйста, выбор", reply_markup=markup)
    elif isinstance(message, CallbackQuery):  # если CallbackQuery - изменяем это сообщение
        call = message
        await call.message.edit_reply_markup(markup)


# функция, которая выдает лиги
async def list_leagues(callback: CallbackQuery, category, **kwargs):
    markup = await leagues_keyboard(category)
    # изменяем сообщение, и отправляем новые кнопки с лигами
    await callback.message.edit_reply_markup(markup)


# функция, которая выдает матчи
async def list_matches(callback: CallbackQuery, category, league, **kwargs):
    markup = await matches_keyboard(category, league)
    # изменяем сообщение, и отправляем новые кнопки с матчами
    await callback.message.edit_text(text="Сделайте, пожалуйста, выбор", reply_markup=markup)


# функция, которая выдает кнопку "сделать ставку"
async def show_match(callback: CallbackQuery, category, league, match_id):
    markup = bet_keyboard(category, league, match_id)
    # берем запись о нашем матче из базы данных
    match = await get_match(match_id)
    text = f"Делайте ставку на матч: {match.name_match}"
    await callback.message.edit_text(text=text, reply_markup=markup)


# функция, которая обрабатывает все нажатия на кнопки
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """
    call: тип объекта CallbackQuery, который прилетает в хендлер
    callback_data: словарь с данными, которые хранятся в нажатой кнопке
    """
    current_level = callback_data.get("level")  # текущий уровень меню
    category = callback_data.get("category")  # текущая категория
    league = callback_data.get("league")  # текущая лига
    match_id = int(callback_data.get("match_id"))  # id матча
    # "уровни" в которых будут отправляться новые кнопки пользователю
    levels = {
        "0": list_categories,  # отдаем категории
        "1": list_leagues,  # отдаем лиги
        "2": list_matches,  # отдаем матчи
        "3": show_match  # предлагаем сделать ставку
    }
    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[current_level]
    # Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    await current_level_function(
        call,
        category=category,
        league=league,
        match_id=match_id
    )
