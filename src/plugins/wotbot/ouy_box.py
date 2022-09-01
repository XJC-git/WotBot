import asyncio

import httpx
from bs4 import BeautifulSoup
from nonebot.log import logger


async def fetch_wotbox(name):
    url = "https://wotbox.ouj.com/wotbox/index.php?r=default/index"
    params = {
        "pn": name
    }
    async with httpx.AsyncClient() as client:
        resp = await client.get(url, params=params, timeout=None)
        result = resp.content
    soup = BeautifulSoup(result, 'lxml')
    power = soup.find(attrs={'class','power fl'}).find(attrs={'class','num'}).text
    power_change = soup.find(attrs={'class','power fl'}).find(attrs={'class','float-num'}).text
    user_data = soup.find(attrs={'class','userRecord-data clearfix'}).children
    damage_average = 0
    exp_average = 0
    kill_average = 0
    for t in user_data:
        if t.text.__contains__('杀伤'):
            damage_average = t.text[2:]
        elif t.text.__contains__('经验'):
            exp_average = t.text[2:]
        elif t.text.__contains__('击毁'):
            kill_average = t.text[2:]
    hit_average = soup.find(attrs={'class','title hit-rate-1k'}).attrs['hit-rate']
    recent_tank_html = soup.findAll(attrs={'class','user-tank__pop'})
    recent_tank = []
    for t in recent_tank_html:
        tank_icon = "https:"+t.find(attrs={'class','tank-pop__icon'}).attrs['src']
        tank_name = t.find(attrs={'class','tank-pop__info'}).find('h3').text
        tank_win_ratio = t.find(attrs={'class','tank-pop__info'}).find(attrs={'class','win num'}).text
        get_power = lambda a: str(a)[str(a).find('战力')+3:]
        tank_power = get_power(t.find(attrs={'class','tank-pop__info'}).find('p').text)
        tank_damage_average = t.find(attrs={'class','tank-pop__body'}).find('p').find(attrs={'class',"data"}).text
        recent_tank.append({
            'tank_icon': tank_icon,
            'tank_name': tank_name,
            'tank_win_ratio': tank_win_ratio,
            'tank_power': tank_power,
            'tank_damage_average': tank_damage_average
        })
    result = {
        'power': power,
        'power_change': power_change,
        'damage_average': damage_average,
        'exp_average': exp_average,
        'hit_average': hit_average,
        'recent_tank': recent_tank,
        'kill_average': kill_average
    }
    return result

if __name__ == '__main__':
    asyncio.run(fetch_wotbox("灵能罐头"))