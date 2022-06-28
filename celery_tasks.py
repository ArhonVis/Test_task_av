# -*- coding: utf-8 -*
from celery import Celery
from celery.utils.log import get_task_logger
from typing import List

from config import redis
from db import database
from scripts.transacts import Transact

celery = Celery(
	'celery_tasks',
	broker=redis.get('broker'),
	backend=redis.get('backend')
)
logger = get_task_logger('celery_tasks')


@celery.task
async def add_transact(keyt_out: int, keyt_in: int, amount: float) -> float:
	try:
		await database.connection()
		logger.info('Transact out: {0}, to: {1}, amount: {2}'.format(keyt_out, keyt_in, amount))
		tr = Transact(database)
		_ = tr.check_poss_transact(keyt_out, keyt_in, amount)
		amount = tr.run_transact(keyt_out, keyt_in, amount)
		return amount
	except Exception as e:
		await database.disconnect()
		raise e
