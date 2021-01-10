import requests
import base64
from time import time
from re import compile
import datetime
from parsel import Selector
from requests.models import HTTPError

class Login:
    cookie_find = compile(r'\.ncov2019selfreport=(.+?);')
    
    def __init__(self, username: str, password: str) -> None:
        self.session = requests.session()
        self.username = username
        self.password = password
        self.urlParam = ''
        self.cookie_location = ''
        self.cookie = ''
        self.headers = Headers()

    def getCookie(self):
        """Get given user's cookies.
        """
        self.__login()
        return self.cookie

    def setUserInfo(self, username, password):
        """Set up user information dynamically.
        """
        if not username or not password:
            raise ValueError('The username and password cannot be None.')
        self.username = username
        self.password = password


    def getUrlParamTail(self):
        """Generate the base64 url param.
        """
        time_tail = '242593854'
        time_start = str(time()).split('.')[0]
        time_str = time_start + time_tail
        data = '{"timestamp":%d,"responseType":"code","clientId":"WUHWfrntnWYHZfzQ5QvXUCVy","scope":"1","redirectUri":"https://selfreport.shu.edu.cn/LoginSSO.aspx?ReturnUrl=%s","state":""}' % (
            int(time_str), r'%2f')

        b64_byt = base64.b64encode(data.encode())
        # 将字节转换成字符
        self.urlParam = b64_byt.decode('utf-8')
        return self.urlParam

    def checkUserInfo(self, username: str, password: str) -> bool:
        """Return False means the UserInfo is discorrect.
        """
        print(username,password)
        self.setUserInfo(username=username, password=password)
        response = self.loginAPI()
        return self.__checkAPI(response.history)

    def __login(self):
        """The concrete implementation of logining process. 
        """
        response = self.loginAPI()
        r_lsit = response.history
        # for each in r_lsit:
        #     print(each.headers)
            
        if not self.__checkAPI(r_lsit):
            raise ValueError('[ERROR]: UserInfo ERROR.')

        cookie = r_lsit[2].headers['Set-Cookie']
        self.cookie = self.__formatCookies(cookie)

# 15122760  1212CYZzy
# 16121337,1997913Was
    def loginAPI(self):
        urlParam = self.getUrlParamTail()
        headers = self.headers.loginHeaders()
        data = {
            'username': self.username,
            'password': self.password,
            'login_submit': ''
        }

        response = self.session.post(
            f'https://newsso.shu.edu.cn/login/{urlParam}', headers=headers, data=data)
        if response.status_code != 200:
            raise HTTPError('Cookies is not 200.')
        return response

    def __checkAPI(self, res_history: list) -> bool:
        """Checking if the 'Set-Cookie' exist in the Headers to check out the userInfo. 
        """
        if len(res_history) < 3:
            return False
        
        for each in res_history:
            # print(each.headers)
            if 'Set-Cookie' in each.headers:
                return True
        return False

    def __formatCookies(self, cookie: str) -> dict:
        if not cookie:
            return
        res = self.cookie_find.search(cookie)
        if not res:
            return 
        key = '.ncov2019selfreport'
        value = res[1]
        return {key: value}

    def getViewState(self):
        yesterday = str(self.getYesterday())
        cookies = self.cookie
        headers = self.headers.getViewStateHeaders()
        params = (
            ('day', yesterday),
            ('t', '2'),
        )
        response = self.session.get('https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx', headers=headers, params=params, cookies=cookies)
        if response.status_code == 200:
            print('Viewstate has been got successfully.')

        html = response.text
        # print(html)
        find = Selector(text=html)
        res  = find.css('#__VIEWSTATE::attr(value)').get()
        # print(res)
        assert res is not None
        return res

    @staticmethod
    def getYesterday(): 
        today=datetime.date.today() 
        oneday=datetime.timedelta(days=1) 
        yesterday=today-oneday  
        return yesterday



class ProxyLogin(Login):
    def __init__(self, username: str, password: str) -> None:
        super().__init__(username, password)
        self.__proxies = self.headers.proxies()

    def setProxies(self,proxy):
        self.__proxies = proxy

    def loginAPI(self):
        urlParam = self.getUrlParamTail()
        headers = self.headers.loginHeaders()
        data = {
            'username': self.username,
            'password': self.password,
            'login_submit': ''
        }
        proxies = {
            "http": self.__proxies,
            "https": self.__proxies,
        }
        response = self.session.post(
            f'https://newsso.shu.edu.cn/login/{urlParam}', headers=headers, data=data,proxies=proxies,timeout=10)
        if response.status_code != 200:
            raise HTTPError('Cookies status is not 200.')
        return response 
        

    def getViewState(self):
        yesterday = str(self.getYesterday())
        cookies = self.cookie
        headers = self.headers.getViewStateHeaders()
        params = (
            ('day', yesterday),
            ('t', '2'),
        )
        proxies = {
            "http": self.__proxies,
            "https": self.__proxies,
        }
        response = self.session.get('https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx', headers=headers, params=params, cookies=cookies, proxies=proxies)
        # response = self.session.get('https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx', headers=headers, params=params, cookies=cookies)
        if response.status_code == 200:
            print('Viewstate has been got successfully.')

        html = response.text
        # print(html)
        find = Selector(text=html)
        res  = find.css('#__VIEWSTATE::attr(value)').get()
        assert res is not None
        return res


class Headers:
    @staticmethod
    def urlParamHeaders():
        return {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }

    @staticmethod
    def loginHeaders():
        return {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Origin': 'https://newsso.shu.edu.cn',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Dest': 'document',
            'Referer': f'https://newsso.shu.edu.cn',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }
        
    @staticmethod
    def getViewStateHeaders():
        return {
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
        
    
    @staticmethod
    def proxies():
    #http代理接入服务器地址端口
        proxyHost = "http-proxy-t3.dobel.cn"
        proxyPort = "9180"

        #账号密码
        proxyUser = "CRAZYHU1AAAKQT80"
        proxyPass = "Ls5qPsJi"

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                "host" : proxyHost,
                "port" : proxyPort,
                "user" : proxyUser,
                "pass" : proxyPass,
        }

        proxies = {
                "http"  : proxyMeta,
                "https" : proxyMeta,
        }
        return proxyMeta

if __name__ == "__main__":
    pass
    # cookie = l_obj.checkUserInfo('20721681','Aa961028')
    
    # print(time())
    # print(l_obj.getUrlParam())
