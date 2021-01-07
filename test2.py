import asyncio
import aiohttp
import requests

def getProxies():
    res = requests.get('http://httpbapi.dobel.cn/User/getIp&account=AYQVKG62gWrj2VjM&accountKey=YqR8Sxc3Jk40&num=4&cityId=all')
    data_json = res.json()
    print(data_json)
    if data_json['code'] != '200':
        raise ValueError('not 200 status_code')
    proxy_data:dict = data_json['data']
    print(proxy_data)
    
    # proxy_data = [{'ip': '218.74.205.144', 'port': '43590', 'left_time': '329s', 'city': '宁波'}, {'ip': '114.100.121.13', 'port': '44101', 'left_time': '329s', 'city': '合肥'}, {'ip': '60.166.97.22', 'port': '43723', 'left_time': '329s', 'city': '合肥'}, {'ip': '123.190.157.42', 'port': '44344', 'left_time': '329s', 'city': '辽阳'}, {'ip': '122.245.156.28', 'port': '44492', 'left_time': '329s', 'city': '宁波'}, {'ip': '115.223.166.66', 'port': '43834', 'left_time': '329s', 'city': '温州'}, {'ip': '27.42.145.242', 'port': '42576', 'left_time': '329s', 'city': '中山'}, {'ip': '106.56.123.50', 'port': '41913', 'left_time': '329s', 'city': '红河'}, {'ip': '115.223.136.107', 'port': '43885', 'left_time': '329s', 'city': '温州'}, {'ip': '218.73.117.154', 'port': '43986', 'left_time': '329s', 'city': '嘉兴'}]
    for each in proxy_data:
        
    # letf_time:str = proxy_data['left_time']
        letf_time:str = each['left_time']
        # 'left_time': '352s'
        proxy = 'http://%(ip)s:%(port)s'%{
            'ip':each['ip'],
            'port':each['port'],
        }
        print(proxy)
        # proxies = {
        # 'http': each['ip'],
        # 'https': each['port']
        # }
        proxies = {
        'http': proxy,
        'https': proxy
        }
        yield proxy,proxies,letf_time

   


# proxy = '218.71.225.135:43429'
# proxies = {
#    'http': 'http://' + proxy,
#    'https': 'https://' + proxy,
# }


# for _,proxies,l_time in getProxies():pass    # print(proxies,l_time)
    # try:
    #     # print(l_time)
    #     # response = requests.get('https://httpbin.org/ip',proxies=proxies)
    #     response = requests.get('https://www.baidu.com/',proxies=proxies,timeout=3)
    #     print(response.text)

    # except Exception as e:
    #     print('Error', e.args)

    # proxy = 'http://140.143.6.16:1080'


async def main():
    async with aiohttp.ClientSession() as session:
        try:
            for proxy,proxies,l_time in getProxies():
                print(proxy)
                async with session.get('http://httpbin.org/ip', proxy=proxy) as response:
                    print(await response.text())
        except Exception as e:
            print('Error：', e.args)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())





