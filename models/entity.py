from gino import Gino
from data.config import POSTGRES_URI

db = Gino()


class League(db.Model):
    __tablename__ = 'league'
    id = db.Column(db.Integer, primary_key=True)
    name_league = db.Column(db.VARCHAR(200), nullable=False)


class Matches(db.Model):
    __tablename__ = 'matches'
    id = db.Column(db.Integer, primary_key=True)
    category_code = db.Column(db.VARCHAR(20))
    category_name = db.Column(db.VARCHAR(50))
    league_code = db.Column(db.VARCHAR(20))
    league_name = db.Column(db.VARCHAR(30))
    name_match = db.Column(db.VARCHAR(50))
    # first_command = db.Column(db.VARCHAR(200), nullable=False)
    # second_command = db.Column(db.VARCHAR(200), nullable=False)
    date_match = db.Column(db.Date)
    league_id = db.Column(db.Integer)
    _table_args__ = (db.ForeignKeyConstraint(['league_id'], ['league.id'],  name='League_id_fk'))


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_telegram_id = db.Column(db.VARCHAR(200), nullable=False) # or db.Column(db.Integer, nullable=False)


class Betting(db.Model):
    __tablename__ = 'betting'
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    first_bet = db.Column(db.VARCHAR(200), nullable=False)
    second_bet = db.Column(db.VARCHAR(200), nullable=False)
    _table_args__ = (db.ForeignKeyConstraint(['match_id'], ['matches.id'],  name='Match_id_fk'),
                     db.ForeignKeyConstraint(['user_id'], ['users.id'], name='User_id_fk'))



async def create_db():
    await db.set_bind(POSTGRES_URI)  # устанавливаем связь с базой данных
    await db.gino.create_all()
    # await db.pop_bind().close()


#asyncio.get_event_loop().run_until_complete(create_db())
