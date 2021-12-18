from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards.menu_keyboards import bet_match


from loader import dp
from models.entity import Betting


class NewBet(StatesGroup):
    Score1 = State()
    Score2 = State()
    Confirm = State()


@dp.callback_query_handler(bet_match.filter())
async def add_item(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await NewBet.Score1.set()
    bet = Betting()
    bet.match_id = int(callback_data.get('match_id'))
    bet.user_id = call.from_user.id
    await call.message.answer("Сколько забьет команда 1:")
    await state.update_data(bet=bet)


@dp.message_handler(state=NewBet.Score1)
async def enter_name(message: types.Message, state: FSMContext):
    first_bet = message.text
    data = await state.get_data()
    bet: Betting = data.get("bet")
    bet.first_bet = first_bet
    await message.answer("Сколько забьет команда 2:")
    await NewBet.Score2.set()
    await state.update_data(bet=bet)


@dp.message_handler(state=NewBet.Score2)
async def add_photo(message: types.Message, state: FSMContext):
    second_bet = message.text
    data = await state.get_data()
    bet: Betting = data.get("bet")
    bet.second_bet = second_bet

    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text="Да", callback_data="confirm")],
            [InlineKeyboardButton(text="Ввести заново", callback_data="change")],
            [InlineKeyboardButton(text="Отменить прогноз", callback_data="cancel")],
        ]
    )
    await message.answer(f"Ваш прогноз: {bet.first_bet} - {second_bet}.\n"
                         f"Подтверждаете прогноз?", reply_markup=markup),

    await NewBet.Confirm.set()
    await state.update_data(bet=bet)


@dp.callback_query_handler(text_contains="change", state=NewBet.Confirm)
async def enter_price(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Сколько забьет команда 1:")
    await NewBet.Score1.set()


@dp.callback_query_handler(text_contains="cancel", state=NewBet.Confirm)
async def cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Вы отменили свой прогноз")
    await state.reset_state()


@dp.callback_query_handler(text_contains="confirm", state=NewBet.Confirm)
async def enter_price(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    bet: Betting = data.get("bet")
    await bet.create()
    await call.message.answer("Ваш прогноз принят!")
    await state.reset_state()
