
import asyncio
import requests
from parsel import Selector
from aiohttp import request


def genurls():
    url = 'https://baidu.com/'

    response = requests.get(url)
    print(response.status_code)
    print(response.headers)

    find = Selector(text=response.text)
    urls = find.css('a::attr(href)').getall()
    for each_url in urls:
        yield each_url
    
    

async def fetch(url:str):
    Headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    }
    print(url)
    try:
        async with request(method='GET',url=url,headers=Headers) as response:
            print(response.status)
    except Exception as e:
        print(e.args)
        

    
def main():
    async def run_1():
        tasks = [asyncio.create_task(fetch(each_url)) for each_url in genurls()]

        await asyncio.gather(*tasks)
        
    asyncio.run(run_1())

if __name__ == "__main__":
    main()
    
# for i in range(10):
#     print(1)
#     break
# else:
#     print(2)
# print(3)