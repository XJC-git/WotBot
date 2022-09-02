from pathlib import Path

import httpx
import jinja2
from nonebot.adapters.onebot.v11 import MessageSegment

from src.plugins.wotbot import color_utils
from src.plugins.wotbot.ouy_box import fetch_wotbox
from nonebot.log import logger

import src.plugins.wotbot.url as url_utils
from nonebot_plugin_htmlrender import html_to_pic

dir_path = Path(__file__).parent
template_path = dir_path / "template"
env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(template_path), enable_async=True
)


async def query_player_by_name(args, bot, ev):
    name = args[0]
    if len(args)>1:
        text = ev.raw_message[ev.raw_message.find(args[0]):]
        name = text
    # 查找玩家
    result = await url_utils.fetch_wotgame_search_user(name)
    wotgame_data: dict = result['response'][0]
    user_id = result['response'][0]['account_id']

    # 获取军团资料
    if result['response'][0]['clan_url'] is not None and len(result['response'][0]['clan_url'])>0:
        clan_url: str = result['response'][0]['clan_url']
        clan_url = clan_url[:clan_url.find("?")] + "api/claninfo/"
        insert_data = await url_utils.fetch_wotgame_clan_info(clan_url)
        wotgame_data.update(insert_data)

    # 获取详细资料
    url = url_utils.PROFILE_SUMMARY

    ouy_data = await fetch_wotbox(name)
    render_data = dict(ouy_data, **wotgame_data)
    render_data.update({'power_color': color_utils.set_power_color(render_data['power'])})
    render_data.update({'win_color': color_utils.set_win_color(render_data['account_wins'])})
    template = env.get_template("wot-player.html")
    template_data = {
        "template_path": template_path,
        "data": render_data
    }
    content = await template.render_async(template_data)
    image = await html_to_pic(content, wait=0, viewport={"width": 920, "height": 1000})
    await bot.send(ev, MessageSegment.image(image))






