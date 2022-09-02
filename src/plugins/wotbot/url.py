import httpx

SEARCH_USER = 'https://wotgame.cn/zh-cn/community/accounts/search/'
PROFILE_SUMMARY = 'https://wotgame.cn/wotup/profile/summary/'


async def fetch_wotgame_search_user(name):
    url = SEARCH_USER
    headers = {
        "x-requested-with": "XMLHttpRequest"
    }
    params = {
        "name": name,
        "name_gt": None
    }
    async with httpx.AsyncClient(headers=headers) as client:
        resp = await client.get(url, params=params, timeout=None)
        result = resp.json()
    return result

async def fetch_wotgame_clan_info(clan_url):
    headers = {
        "x-requested-with": "XMLHttpRequest"
    }
    async with httpx.AsyncClient(headers=headers) as client:
        resp = await client.get(clan_url, timeout=None)
        result = resp.json()
    return {'clan_color': result['clanview']['clan']['color']}