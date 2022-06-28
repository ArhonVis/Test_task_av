# -*- coding: utf-8 -*
import sqlalchemy

metadata = sqlalchemy.MetaData()


balance_table = sqlalchemy.Table(
    "user_balance",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("balance", sqlalchemy.Float),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column('removed', sqlalchemy.Boolean(), default=False, nullable=False)
)
