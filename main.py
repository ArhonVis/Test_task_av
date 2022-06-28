# -*- coding: utf-8 -*
from fastapi import FastAPI
from celery_tasks import add_transact
from db import database
from scripts import users
from scripts.user_balance import BalanceIncorrect, KeytNotFound
from scripts.user_balance import Balance

app = FastAPI()


@app.on_event("startup")
async def startup():
	await database.connect()


@app.on_event("shutdown")
async def shutdown():
	await database.disconnect()


@app.get("/")
async def root():
	return {"msg": "Hello"}


@app.get("/hello/{name}")
async def say_hello(name: str):
	return {"msg": f"Hello {name}"}


@app.post("/transact_add")
async def add_transact(keyt_out: int, keyt_in: int, amount: float):
	task = await add_transact.delay(keyt_out=keyt_out, keyt_in=keyt_in, amount=amount)
	if task.result in [BalanceIncorrect, KeytNotFound]:
		return {
			'msg': "Error",
			'details': f'{0}'.format(task.result.ERROR_CUSTOM_TEXT)
		}
	elif task.status == "SUCCESS":
		return {
			'msg': f'SUCCESS, new balance: {0}'.format(task.result)
		}
	else:
		return {
			'msg': "Error"
		}


@app.post('/user_add')
async def add_user(email: str, name: str, hashed_password: str):
	user = users.User(database)
	uid = await user.add_user(
		email=email,
		name=name,
		hashed_password=hashed_password
	)
	
	_ = await database.execute("COMMIT;")
	return {
		'msg': {f'uid: {uid}'}
	}


@app.post('/keyt_add')
async def add_keyt(uid):
	ub = Balance(database)
	kid = await ub.add_keyt(uid=uid)
	_ = await database.execute("COMMIT;")
	return {
		'msg': f"Create keyt {kid}"
	}


@app.post('/keyt_delete')
async def del_keyt(kid):
	ub = Balance(database)
	kid = await ub.delete_keyt(kid=kid)
	_ = await database.execute("COMMIT;")
	return {
		'msg': f"Delete keyt {kid}"
	}


# For test
@app.post('/balance_add')
async def balance_update(kid: int, amount: float):
	ub = Balance(database)
	kid = await ub.update_balance(kid=kid, diff_amount=amount)
	_ = await database.execute("COMMIT;")
	return {
		'msg': f"Balance update. Now balance: {kid}"
	}


@app.delete('/user_dell')
async def del_user(uid: int):
	user = users.User(database)
	_ = await user.delete_user(uid=uid)
	ub = Balance(database)
	_ = await ub.delete_user_keyt(uid=uid)
	_ = await database.execute("COMMIT;")
	return {
		'msg': f"User {uid} was deleted"
	}
