# -*- coding: utf-8 -*
from scripts import user_balance


class Transact:
	def __init__(self, db):
		self.db = db
	
	async def check_poss_transact(self, keyt_out: int, keyt_in: int, amount: float):
		ub = user_balance.Balance(self.db)
		_ = await ub.check_balance(kid=keyt_out, diff_amount=-amount)
		_ = await ub.check_balance(kid=keyt_in, diff_amount=amount)
		return True
	
	async def run_transact(self, keyt_out: int, keyt_in: int, amount: float) -> float:
		ub = user_balance.Balance(self.db)
		amount = await ub.update_balance(kid=keyt_out, diff_amount=-amount)[0]
		_ = await ub.update_balance(kid=keyt_in, diff_amount=amount)
		return amount
