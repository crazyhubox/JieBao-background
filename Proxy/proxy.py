import asyncio
import requests
from aiohttp import ClientSession, ClientTimeout, request
from redis import Redis
import time

now = lambda :int(time.time())

# This base class has defined some functions used frequently.
class BaseProxy:
    def __init__(self) -> None:
        self.rdb = Redis(host='', password='', db=0, decode_responses=True)
        self.localredis = Redis(host='127.0.0.1', db=0, decode_responses=True)
        self.proxy = ''
        self.RawProxiesTable = 'RawProxies'
        self.availbleProxiesTable = 'availbleProxies'
        self.timeout = False

    def getRawProxies(self):
        res = self.rdb.hgetall(self.RawProxiesTable)
        for proxy, t in res.items():
            yield proxy, t


    def getAvailableProxies(self, num: int = -1):
        assert num > -2
        res = self.rdb.hgetall(self.availbleProxiesTable)
        if num == -1:
            for proxy, t in res.items():
                yield proxy, t
        else:
            for proxy, t in res.items():
                yield proxy, t
                num -= 1
                if num == 0:
                    break

    def initRawTable(self):
        kes = self.rdb.hkeys(self.RawProxiesTable)
        if not kes:
            return
        results = self.rdb.hdel(self.RawProxiesTable, *kes)
        if results:
            print('[INFO]:The RawTable has initialized.')
            
            
    def initAvailableTable(self):
        kes = self.rdb.hkeys(self.availbleProxiesTable)
        if not kes:
            return
        results = self.rdb.hdel(self.availbleProxiesTable, *kes)
        if results:
            print('[INFO]:The AvailbleProxiesTable has initialized.')

# The proxy class operate the proxies on the server.
class Proxy(BaseProxy):
    
    def genRawProxies(self):
        res = requests.get(
            'http://httpbapi.dobel.cn/User/getIp&account=AYQVKG62gWrj2VjM&accountKey=YqR8Sxc3Jk40&num=2&cityId=all')
        data_json = res.json()
        print(data_json)
        if data_json['code'] != '200':
            raise ValueError('Not 200 status_code')
        proxy_data: dict = data_json['data']
        print(proxy_data)

        for each in proxy_data:
            letf_time: str = each['left_time']
            proxy = 'http://%(ip)s:%(port)s' % {
                'ip': each['ip'],
                'port': each['port'],
            }
            yield proxy, letf_time

    
    async def fetch(self, url, proxy_info: tuple, timeout=None):
        ip_port = proxy_info[0]
        t = proxy_info[1]
        proxy = f'{ip_port}'
        try:
            async with request(method='GET', url=url,proxy=proxy) as resp:
                print(await resp.read())
        except Exception as e:
            print(e.args)
        else:
            res = self.rdb.hset(self.availbleProxiesTable, ip_port, t)
            if res:
                print(f'[INFO]: This proxy is available.{ip_port},It has been added into redis.')
        finally:
            self.rdb.hdel(self.RawProxiesTable, proxy)


    def cleanTime(self,left_time:str)->int:
        left_time = int(left_time.replace('s',''))
        return now() + left_time - 60

    def Extract(self):
        self.initRawTable()
        for each_p, t in self.genRawProxies():
            self.rdb.hset(self.RawProxiesTable, each_p, self.cleanTime(t))
            print(f'[Extract]:{each_p}')

    def Verify(self):
        async def run_main():
            timeout = ClientTimeout(sock_read=10)
            tasks = [self.fetch(url='http://selfreport.shu.edu.cn', proxy_info=(p, t)) for p, t in
                     self.getRawProxies()]
            await asyncio.gather(*tasks)

        self.initAvailableTable()
        asyncio.run(run_main())


    def Scan(self):
        async def f():
            timeout = ClientTimeout(sock_connect=10)
            proxies = tuple([p for p, _ in self.getAvailableProxies()])
            tasks = [asyncio.create_task(self.check('http://selfreport.shu.edu.cn', each, timeout=timeout)) for each, _
                     in
                     self.getRawProxies()]
            await asyncio.gather(*tasks)
        # 全部扫一遍,一个死其他也差不多了
        loop =  asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(f())
        except Exception as e:
            print(e.args)
        finally:
            loop.close()
            return self.timeout
        
    
    async def check(self, url, proxy: str, timeout=None):
        try:
            async with request(method='GET', url=url,
                               proxy=proxy, ) as resp:
                # print(await resp.read())
                await resp.read()
        except Exception as e:
            self.timeout = True
            print(f'[INFO]: This proxy is erro.{proxy}', e.args)
            self.initRawTable()
            all_tasks = asyncio.all_tasks()
            for each_task in all_tasks:
                each_task.cancel()
            # loop = asyncio.get_running_loop()
            # loop.close()

    def ExtractAvailable(self):
        async def f():
            timeout = ClientTimeout(sock_connect=10)
            proxies = tuple([p for p, _ in self.getAvailableProxies()])
            tasks = [asyncio.create_task(self.check('http://selfreport.shu.edu.cn', each, timeout=timeout)) for each, _
                     in
                     self.getAvailableProxies()]
            await asyncio.gather(*tasks)

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(f())
        except Exception as e:
            print(e.args)
        finally:
            loop.close()

        return self.proxy

# The proxy class save the proxies extracted from the api on the localhost 
# and save the available proxies on the server.
class ProxyLocal(Proxy):
    # 先把连接包吃住在本地的rawproxy中，然后检测
    def __init__(self):
        super(ProxyLocal, self).__init__()
        self.localredis = Redis(host='127.0.0.1', db=0, decode_responses=True)

    def initRawTable(self):
        kes = self.localredis.hkeys(self.RawProxiesTable)
        if not kes:
            return
        results = self.localredis.hdel(self.RawProxiesTable, *kes)
        if results:
            print('[INFO]:The RawTable has initialized.')

    def getRawProxies(self):
        res = self.localredis.hgetall(self.RawProxiesTable)
        for proxy, t in res.items():
            yield proxy, t

    def Extract(self):
        self.initRawTable()
        for each_p, t in self.genRawProxies():
            self.localredis.hset(self.RawProxiesTable, each_p, self.cleanTime(t))
            print(f'[Extract]:{each_p}')

    async def fetch(self, url, proxy_info: tuple, timeout=None):
        ip_port = proxy_info[0]
        t = proxy_info[1]
        proxy = f'{ip_port}'
        try:
            async with request(method='GET', url=url,
                               proxy=proxy) as resp:
                print(await resp.read())
        except Exception as e:
            print(e.args)
        else:
            res = self.rdb.hset(self.availbleProxiesTable, ip_port, t)
            if res:
                print(f'[INFO]: This proxy is available.{ip_port},It has been added into redis.')
        finally:
            self.localredis.hdel(self.RawProxiesTable, proxy)


def main():
    # p_obj = ProxyLocal()
    p_obj = Proxy()
    # p_obj.Extract()
    print(p_obj.Scan())
    # p_obj.Verify()
    # res = p_obj.cleanTime('225s')
    # print(res)

if __name__ == '__main__':
    main()

