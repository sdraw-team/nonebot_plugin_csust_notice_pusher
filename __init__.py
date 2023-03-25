from .config import Config
from .page_parser import PageParser
from .db import CachedNotice
from .notice import Notice
import os
from pathlib import Path
import aiohttp
from nonebot_plugin_apscheduler import scheduler
import nonebot
from nonebot import on_command, require
from nonebot.log import logger
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11.adapter import Message, MessageSegment
from nonebot.adapters.onebot.v11 import Message, MessageSegment, Bot, MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg

require("nonebot_plugin_apscheduler")


notice_pusher = on_command("csust_notice_pusher", rule=Rule(), priority=5)
PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = Path().absolute() / "data" / "notice_pusher"
DB_PATH = DATA_PATH / "cache.db"
GLOBAL_CFG = nonebot.get_driver().config
CFG = Config.parse_obj(GLOBAL_CFG.dict())

XGDT_URL = 'https://www.csust.edu.cn/gjxy/xgdt.htm'
XFZX_URL = 'https://www.csust.edu.cn/gjxy/xxyfzzx.htm'
URL_PREFIX = 'https://www.csust.edu.cn/gjxy/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
}

logger.info('加载数据库文件: ' + str(DB_PATH))
db = CachedNotice(DB_PATH)


async def check_and_push():
    msg = await auto_check()
    await push_all(msg)


async def auto_check() -> list[str]:
    msgs = []
    xgdt_notices = await get_notices(XGDT_URL)
    xfzx_notices = await get_notices(XFZX_URL)
    xgdt_updates = []
    xfzx_updates = []

    # 学工动态
    for i, n in enumerate(xgdt_notices):
        if db.is_notice_exists(n.id):
            continue
        full_url = URL_PREFIX + n.url
        msg = f'{i+1}. \n标题：{n.title}\n内容预览：{n.content_preview[:40]}\n链接：{full_url}\n\n'
        xgdt_updates.append(msg)
        db.add_notice(Notice(*n.get_properties()))
        logger.info("学工动态更新: " + msg)
    # 学发中心
    for i, n in enumerate(xfzx_notices):
        if db.is_notice_exists(n.id):
            continue
        full_url = URL_PREFIX + n.url
        msg = f'{i+1}. \n标题：{n.title}\n内容预览：{n.content_preview[:40]}\n链接：{full_url}\n\n'
        xfzx_updates.append(msg)
        db.add_notice(Notice(*n.get_properties()))
        logger.info("学发中心更新: " + msg)

    if xgdt_updates:
        msgs.append('学工动态更新：\n')
        msgs += xgdt_updates

    if xfzx_updates:
        msgs.append('学发中心更新：\n')
        msgs += xfzx_updates

    return msgs


async def get_notices(url: str):
    page_content = await get_page(url)
    if not page_content:
        return

    parser = PageParser(page_content)
    notices = parser.get_notices()

    return notices


async def get_page(url: str) -> str:
    """获取页面

    Raises:
        IOError: 页面获取失败
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=HEADERS) as res:
            if res.status != 200:
                raise IOError('页面获取失败: Code ' + res.status)
            return await res.text()


async def push_all(msg: str):
    for gid in CFG.notice_pusher_enable:
        await push_to_group(gid, msg)


async def push_to_group(groupid: int, msg: str):
    bot = nonebot.get_bot()
    await bot.send_group_msg(group_id=groupid, message=Message(msg))


async def push_error_to_admins(user_id: list[int], msg: str):
    bot = nonebot.get_bot()
    for u in user_id:
        await bot.send_private_msg(user_id=user_id, message=Message(msg))

scheduler.add_job(
    check_and_push,
    'cron',
    hour=9,
    minute=0,
    second=0,
    id='check_notice_and_push'
)


@notice_pusher.handle()
async def handle_pusher(matcher: Matcher, event: MessageEvent, arg: Message = CommandArg()):
    try:
        msg = await auto_check()
    except IOError as e:
        await push_error_to_admins(GLOBAL_CFG.superusers, str(e))
        return

    await matcher.finish(msg)
