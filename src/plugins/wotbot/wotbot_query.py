from pathlib import Path

import httpx
import jinja2
from nonebot.adapters.onebot.v11 import MessageSegment
from src.plugins.wotbot.ouy_box import fetch_wotbox
from nonebot.log import logger

import src.plugins.wotbot.url as static
from nonebot_plugin_htmlrender import html_to_pic

dir_path = Path(__file__).parent
template_path = dir_path / "template"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path), enable_async=True
)


async def query_player_by_name(args, bot, ev):
    name = ''
    for i in args:
        name += i
    # 查找玩家
    url = static.SEARCH_USER
    headers = {
        "x-requested-with": "XMLHttpRequest"
    }
    params = {
        "name": args[0],
        "name_gt": None
    }
    async with httpx.AsyncClient(headers=headers) as client:
        resp = await client.get(url, params=params, timeout=None)
        result = resp.json()
    wotgame_data: dict = result['response'][0]
    user_id = result['response'][0]['account_id']

    # 获取军团资料
    clan_url: str = result['response'][0]['clan_url']
    clan_url = clan_url[:clan_url.find("?")] + "api/claninfo/"
    async with httpx.AsyncClient(headers=headers) as client:
        resp = await client.get(clan_url, timeout=None)
        result = resp.json()
    wotgame_data.update({'clan_color': result['clanview']['clan']['color']})

    # 获取详细资料
    url = static.PROFILE_SUMMARY

    ouy_data = await fetch_wotbox(name)
    render_data = dict(ouy_data, **wotgame_data)
    template = env.get_template("wot-player.html")
    template_data = {
        "template_path": template_path,
        "data": render_data
    }
    content = await template.render_async(template_data)
    image = await html_to_pic(content, wait=0, viewport={"width": 920, "height": 1000})
    await bot.send(ev, MessageSegment.image(image))
