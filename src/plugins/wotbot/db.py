from dataclasses import dataclass

from nonebot import logger
from peewee import *

db = SqliteDatabase('database.db')
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


class UserBind(BaseModel):
    id = IntegerField()
    qq = TextField()
    name = TextField()


@dataclass
class ExecuteResult:
    result: bool
    msg: str


def check_database():
    global db
    logger.debug("正在初始化数据库连接")
    if db is None:
        db = SqliteDatabase('database.db')
        db.connect()
    tables = db.get_tables()
    if 'userbind' not in tables:
        db.create_tables([UserBind])


def insert_user_bind(qq, name):
    current_id = 0
    try:
        exist_record = UserBind.select().where(UserBind.qq == qq, UserBind.name == name)
        if exist_record is not None and len(exist_record) > 0:
            return ExecuteResult(False, "已绑定过此账号")
    except DoesNotExist:
        pass
    try:
        previous_record = UserBind.select().where(UserBind.qq == qq)
        current_id = len(previous_record)
    except DoesNotExist:
        current_id = 0
    if current_id < 20:
        try:
            UserBind.create(id=current_id, qq=qq, name=name)
        except:
            return ExecuteResult(False, "数据库操作失败，请查看日志")
        return ExecuteResult(True, "")
    else:
        return ExecuteResult(False, "账号绑定数量已达上限(20)")


def query_user_bind(qq):
    try:
        record = UserBind.select().where(UserBind.qq == qq).order_by(UserBind.name)
        if record is not None and len(record) > 0:
            return ExecuteResult(True, record)
    except DoesNotExist:
        return ExecuteResult(False, "没有找到绑定信息")



