#!/usr/bin/python
# -*- coding: utf-8 -*-
import aiohttp
import asyncio
import json


class ProxyGrabber:
    def __init__(self):
        super().__init__()
        print('Country')
        self.country = str(input())
        print('Proxy Type')
        self.proxytype = str(input())
        self.proxies = []
        asyncio.run(self.main())

    async def proxyscrape(self, session, country, proxytype):
        url = f'https://api.proxyscrape.com/?request=displayproxies&proxytype={proxytype}&country={country}'
        try:
            async with session.get(url) as response:
                r = await response.text()
                proxies = r.split('\r\n')
                for proxy in proxies:
                    self.proxies.append(proxy)
        except Exception as e:
            print(f'Site: proxyscrape.com\n{e}')

    async def proxyscan(self, session, country, proxytype):
        url = f'https://www.proxyscan.io/api/proxy?country={country}&limit=10&type={proxytype}'
        try:
            async with session.get(url) as response:
                r = await response.read()
                json_body = json.loads(r)
                for item in json_body:
                    proxy = f"{item['Ip']}:{item['Port']}"
                    self.proxies.append(proxy)
        except Exception as e:
            print(f'Site: proxyscan.io\n{e}')

    async def pubproxy(self, session, country, proxytype):
        url = f'http://pubproxy.com/api/proxy?limit=5&type={proxytype}&country={country}'
        try:
            async with session.get(url) as response:
                r = await response.read()
                json_body = json.loads(r)
                for item in json_body['data']:
                    proxy = f"{item['ipPort']}"
                    self.proxies.append(proxy)
        except Exception as e:
            print(f'Site: pubproxy.com\n{e}')

    async def freshproxies(self, session, country, proxytype):
        url = f'https://www.freshproxies.net/ProxyList?countries_1={country}&protocol={proxytype}&format=json&count=20'
        try:
            async with session.get(url) as response:
                r = await response.read()
                json_body = json.loads(r)
                for item in json_body['proxies']:
                    proxy = f"{item['ip']}:{item['port']}"
                    if not proxy.startswith('0.0.0.0'):
                        self.proxies.append(proxy)
        except Exception as e:
            print(f'Site: freshproxies.net\n{e}')

    async def proxy_list(self, session, country, proxytype):
        url = f'https://www.proxy-list.download/api/v1/get?type={proxytype}&country={country}'
        try:
            async with session.get(url) as response:
                r = await response.text()
                proxies = r.split('\r\n')
                for proxy in proxies:
                    self.proxies.append(proxy)
        except Exception as e:
            print(f'Site: www.proxy-list.download\n{e}')

    def create_txt(self, proxies):
        proxies = list(set(proxies))
        with open(f'{self.country}_{self.proxytype}.txt', 'a') as f:
            for proxy in proxies:
                if proxy != '':
                    f.write(f'{proxy}\n')

    async def main(self):

        async with aiohttp.ClientSession() as session:
            task_1 = asyncio.create_task(self.pubproxy(session, self.country, self.proxytype))
            task_2 = asyncio.create_task(self.proxyscan(session, self.country, self.proxytype))
            task_3 = asyncio.create_task(self.proxyscrape(session, self.country, self.proxytype))
            task_4 = asyncio.create_task(self.freshproxies(session, self.country, self.proxytype))
            task_5 = asyncio.create_task(self.proxy_list(session, self.country, self.proxytype))

            await asyncio.gather(task_1, task_2, task_3, task_4, task_5)

            self.create_txt(self.proxies)


if __name__ == '__main__':
    ProxyGrabber()
