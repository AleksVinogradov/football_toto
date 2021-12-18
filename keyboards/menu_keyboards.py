from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_commands import get_leagues, get_matches, get_categories

# CallbackData-объекты для работы с меню
menu_cd = CallbackData("show_menu", "level", "category", "league", "match_id")
bet_match = CallbackData("bet", "match_id")


# формируем коллбек дату для каждого элемента меню, в зависимости от переданных параметров
def make_callback_data(level, category="0", league="0", match_id="0"):
    return menu_cd.new(level=level, category=category, league=league, match_id=match_id)


# функция, которая отдает клавиатуру с доступными категориями
async def categories_keyboard():
    CURRENT_LEVEL = 0  # текущий уровень меню - 0
    markup = InlineKeyboardMarkup()  # создаем клавиатуру
    categories = await get_categories()  # список из базы данных с разными категориями
    for category in categories:
        button_text = f"{category.category_name}"  # текст, который будет на кнопке
        # формируем колбек дату, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1, category=category.category_code)
        # вставляем кнопку в клавиатуру
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    return markup  # возвращаем созданную клавиатуру в хендлер


# функция, которая отдает клавиатуру с лигами
async def leagues_keyboard(category):
    CURRENT_LEVEL = 1  # текущий уровень меню - 1
    markup = InlineKeyboardMarkup()  # создаем клавиатуру
    leagues = await get_leagues(category)  # список из базы данных с разными лигами
    for league in leagues:
        button_text = f"{league.league_name}"  # текст, который будет на кнопке
        # формируем колбек дату, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category, league=league.league_code)
        markup.insert(
            InlineKeyboardButton(text=button_text, callback_data=callback_data)
        )
    # создаем Кнопку "Назад"
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1))
    )
    return markup


# функция, которая отдает клавиатуру с матчами
async def matches_keyboard(category, league):
    CURRENT_LEVEL = 2
    markup = InlineKeyboardMarkup(row_width=1)  # row_width = 1 (одна кнопка в строке)
    matches = await get_matches(category, league)  # список из базы данных с разными матчами
    for match in matches:
        button_text = f"{match.name_match}"  # текст, который будет на кнопке
        # формируем колбек дату, которая будет на кнопке
        callback_data = make_callback_data(level=CURRENT_LEVEL + 1,
                                           category=category, league=league,
                                           match_id=match.id)
        markup.insert(
            InlineKeyboardButton(
                text=button_text, callback_data=callback_data)
        )
    # создаем кнопку "Назад"
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             category=category))
    )
    return markup


# функция, которая отдает клавиатуру с кнопками "ставка" и "назад" для выбранного матча
def bet_keyboard(category, league, match_id):
    CURRENT_LEVEL = 3
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text=f"Ставка", callback_data=bet_match.new(match_id=match_id)
        )
    )
    markup.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=make_callback_data(level=CURRENT_LEVEL - 1,
                                             category=category, league=league))
    )
    return markup
