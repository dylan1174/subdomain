import requests
import common
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import time
'''
    1.传入一个域名
    2.获得总页数
    3.遍历所有的页取出子域名放入列表subdomains
    4.调用common方法保存列表到json文件中
'''

sem = asyncio.Semaphore(10)

def get_urls(domain):
    urls = []
    url = 'https://tool.chinaz.com/subdomain?domain=' + domain
    # 得到一个总页数
    try:
        r = requests.get(url=url)
        soup = BeautifulSoup(r.text, features='lxml')
        pages = soup.find(name='span', attrs={'class': 'col-gray02'})
        s = pages.string
        index_p = s.index('页')
        page = int(s[1:index_p])
        print('chinaz查询总页数:' + str(page))
        # 得到所有的结果页面url
        for i in range(1, page + 1):
            urls.append('https://tool.chinaz.com/subdomain?domain=' + domain + '&page=' + str(i))
        return urls
    except AttributeError:
        print('chinaz收集失败，没有查询到相关的子域名')
        return None


async def spider2(url, subdomains):
    # print('正在请求',url)
    async with(sem):
        async with aiohttp.ClientSession() as session:
            async with session.request('GET', url) as resp:
                # print(resp.status)
                # 解析网页这个行为可以被切换不用一直等待
                content = await resp.text()
                # 从aiohttp response中解析出子域名的链接
                soup = BeautifulSoup(content, features='lxml')
                subs = soup.find_all(name='div', attrs={'class': 'w23-0 subdomain'})
                for sub in subs:
                    # print(sub.a.string)
                    subdomains.append(sub.a.string)

class chinaz(object):
    def __init__(self, domain):
        self.domain = domain

    def run(self):
        st = time.time()
        print('begin to collect from chinaz:{}'.format(time.strftime('%X')))
        subdomains = []
        urls = get_urls(self.domain)
        if not urls:
            return
        # 打包任务 并开启事件循环
        coroutines = []
        for url in urls:
            coroutines.append(spider2(url, subdomains))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(coroutines))
        # 将得到的subdomains结果数组保存
        path = common.get_result(domain=self.domain, type='chinaz.json')
        common.save_result(path, subdomains)
        print('end to collect from chinaz:{}   共计用时{:.2f}s'.format(time.strftime('%X'), time.time()-st))

