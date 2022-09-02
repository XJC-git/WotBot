from dataclasses import dataclass
from typing import Tuple, Protocol

from src.plugins.wotbot.wotbot_query import query_player_by_name
from src.plugins.wotbot.wotbot_bind import bind_player,query_player

class Func(Protocol):
    async def __call__(self, **kwargs):
        ...


@dataclass
class Command:
    keywords: Tuple[str, ...]
    child_command: None
    func: Func
    default_func: Func = None


command_list = [
    Command(('player', '查询玩家', '玩家'), None, query_player_by_name),
    Command(('bind','绑定','绑定账号'),None,bind_player),
    Command(('query','查询绑定'),None,query_player)
]


def search_in_list(keyword, list):
    for command in list:
        if keyword in command.keywords:
            return command


async def match_command(args,bot,ev):
    search_list = command_list
    args_position = 0
    target_command = None
    while search_list is not None:
        res = search_in_list(args[args_position],search_list)
        if res is None:
            break
        search_list = res.child_command
        args_position += 1
        target_command = res
    if target_command.func is not None:
        await target_command.func(args[args_position:],bot,ev)
