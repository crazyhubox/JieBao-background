import requests
from parsel import Selector, selector
from Requets import Login


l_obj = Login(...,...)
l_obj.setUserInfo('16123113','130E2d898')

cookies = l_obj.getCookie()

# cookies = {
#     '.ncov2019selfreport': 'FB07CABFFBC1B1BD5FD60B431089663C79BB9DCA8C67AB0946C911D98FB1D2E567D0596C1EBF4D66F960EB27DCF13B15C39DD9AA9E4640ADFCCCD9F69E63EE30B90D6BB7FE6CD97323830C05CCAAC06E9CB8F8C191ECE55EA1828C7520131E6ACF99977E37DCAA17D236D1BE0A3AA909',
# }

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://selfreport.shu.edu.cn/Default.aspx',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}

response = requests.get('https://selfreport.shu.edu.cn/DayReport.aspx', headers=headers, cookies=cookies)


html = response.text
find = Selector(text=html)

VIEWSTATE = find.css('input[name=__VIEWSTATE]::attr(value)').get()
