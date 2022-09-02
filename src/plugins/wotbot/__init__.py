import html

from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, Bot
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

from src.plugins.wotbot import static
from src.plugins.wotbot.command import match_command
from src.plugins.wotbot.db import check_database

wotbot = on_command("wotbot", aliases={"WOTBOT"}, priority=5)
check_database()

@wotbot.handle()
async def handle_main_command(bot: Bot, ev: MessageEvent, args: Message = CommandArg()):
    if len(args) == 0:
        await bot.send(ev, static.MSG_DEFAULT, at_sender=True)
    else:
        args = html.unescape(str(args)).strip()
        args = args.split(" ")
        await match_command(args, bot, ev)

