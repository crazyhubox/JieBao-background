import requests
from parsel import Selector
import datetime

def getViewState(cookies_:dict):
    # cookies = {
    #     '.ncov2019selfreport': 'ACA21E1E519B7BEE4807C1A024F0ADCF9CC6F524BB7FCAE0222D1B26E57D741D11662FE301591CA17A01777ADF139C673EC4EAD63FDB923C5CFD2CE594B27D64B979EBBFC59DAA21A593033FA7064C120218DD39070BF30AA9F1B7B9D130EE561674C8B8A221744151BD00526F6B25E6',
    # }
    yesterday = str(getYesterday())
    cookies = cookies_
    headers = {
        'Host': 'selfreport.shu.edu.cn',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://selfreport.shu.edu.cn/XueSFX/HalfdayReport_History.aspx',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    params = (
        ('day', yesterday),
        ('t', '2'),
    )

    response = requests.get('https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx', headers=headers, params=params, cookies=cookies)
    if response.status_code == 200:
        print('Viewstate has been got successfully.')

    html = response.text

    # print(html)
    find = Selector(text=html)
    res  = find.css('#__VIEWSTATE::attr(value)').get()

    return res

def getYesterday(): 
    today=datetime.date.today() 
    oneday=datetime.timedelta(days=1) 
    yesterday=today-oneday  
    return yesterday


if __name__ == "__main__":
    # print(str(getYesterday()))
    print(getViewState(''))