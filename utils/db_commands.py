from typing import List
from sqlalchemy import and_
from models.entity import Matches


# функция для создания нового матча в базе данных
async def add_match(**kwargs):
    new_match = await Matches(**kwargs).create()
    return new_match


# функция для вывода разных категорий
async def get_categories() -> List[Matches]:
    return await Matches.query.distinct(Matches.category_name).gino.all()


# функция для вывода лиг в выбранной категории
async def get_leagues(category) -> List[Matches]:
    return await Matches.query.distinct(Matches.league_name).where(Matches.category_code == category).gino.all()


# функция вывода всех матчей выбранной лиги
async def get_matches(category_code, league_code) -> List[Matches]:
    match = await Matches.query.where(
        and_(Matches.category_code == category_code,
             Matches.league_code == league_code)
    ).gino.all()
    return match


# функция для получения объекта матча по его id
async def get_match(match_id) -> Matches:
    match = await Matches.query.where(Matches.id == match_id).gino.first()
    return match
