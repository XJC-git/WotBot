from nonebot import logger
from src.plugins.wotbot.db import *
import src.plugins.wotbot.url as url_utils


async def bind_player(args, bot, ev):
    name = args[0]
    if len(args) > 1:
        text = ev.raw_message[ev.raw_message.find(args[0]):]
        name = text
    result = await url_utils.fetch_wotgame_search_user(name)
    if 'response' not in result or len(result['response']) == 0:
        await bot.send(ev, "绑定失败，没有找到此账号，请检查账号名")
        return
    result = insert_user_bind(ev.user_id, name)
    if result.result:
        await bot.send(ev, "绑定成功")
    else:
        await  bot.send(ev, result.msg)


async def query_player(args, bot, ev):
    name = ''
    for i in args:
        name += i
    result = query_user_bind(ev.user_id)
    if result:
        msg = "当前绑定查询结果为:\n"
        id = 0
        for r in result.msg:
            msg += '{} {}\n'.format(id, r.name)
            id+=1
        await bot.send(ev, msg)
    else:
        await bot.send(ev, result.msg)

async def delete_player(args,bot,ev):
    id = int(args[0])

