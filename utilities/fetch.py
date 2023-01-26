from async_retrying import retry
from apps.ipo.agents import get_user_agents


@retry(attempts=100)
async def fetcher(session, url):
    header = await get_user_agents()
    async with session.get(url, headers=header) as resp:
        resp_text = await resp.text()
        return resp_text
