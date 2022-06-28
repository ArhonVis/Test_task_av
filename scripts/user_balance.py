# -*- coding: utf-8 -*
from typing import Tuple
from sqlalchemy import and_

from models.user_balance import balance_table


class KeytNotFound(BaseException):
	ERROR_CUSTOM_TEXT = "Keyt not found"


class BalanceIncorrect(BaseException):
	ERROR_CUSTOM_TEXT = "Insufficient funds on the balance sheet"


class Balance:
	def __init__(self, db):
		self.db = db
	
	async def add_keyt(self, uid) -> int:
		query = (balance_table.insert().values(
			uid=uid,
			removed=False,
			balance=0.0
		).returning(balance_table.c.id))
		kid = await self.db.fetch_one(query)
		return kid[0]
	
	async def delete_keyt(self, kid: int):
		query = balance_table.update().values(removed=True).where(balance_table.c.id == kid)
		res = await self.db.execute(query)
		return True
	
	async def delete_user_keyt(self, uid: int):
		query = balance_table.update().values(removed=True).where(balance_table.c.uid == uid)
		res = await self.db.execute(query)
		return True
	
	async def update_balance(self, kid: int, diff_amount: float) -> float:
		query = (balance_table.update().values(
			amount=(balance_table.c.balance + diff_amount)
		).where(
			and_(balance_table.c.id == kid, balance_table.c.removed == False)).returning(balance_table.c.balance))
		balance = await self.db.fetch_one(query)[0]
		return balance
	
	async def check_balance(self, kid: int, diff_amount: float):
		query = balance_table.select(
			balance_table.c.balance
		).where(
			and_(
				balance_table.c.id == kid,
				balance_table.c.removed == False))
		amount = await self.db.fetch_one(query)
		if len(amount) == 0:
			raise KeytNotFound
		else:
			amount = amount[0]
		if (amount + diff_amount) < 0:
			raise BalanceIncorrect
