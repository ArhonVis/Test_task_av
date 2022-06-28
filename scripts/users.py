# -*- coding: utf-8 -*
from models.users import users_table


class User:
	def __init__(self, db):
		self.db = db
	
	async def add_user(self, email: str, name: str, hashed_password: str) -> int:
		query = (users_table.insert().values(
			email=email,
			name=name,
			hashed_password=hashed_password,
			removed=False
		).returning(users_table.c.id)
		)
		user_id = await self.db.fetch_one(query)
		return user_id[0]
	
	async def delete_user(self, uid: int):
		query = users_table.update().values(removed=True).where(users_table.c.id == uid)
		res = await self.db.execute(query)
		return True
