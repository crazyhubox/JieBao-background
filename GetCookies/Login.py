import requests
from requests.models import HTTPError
import base64
from time import time


class Login:
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

    def __getUrlParam(self):
        """This functon is used for tests.
        """
        headers = self.headers.urlParamHeaders()
        response = self.session.get(
            'http://selfreport.shu.edu.cn/', headers=headers)
        print(response.status_code)
        r_lsit = response.history
        url_param = r_lsit[3].headers['location']
        cookies = r_lsit[3].headers['set-cookie']
        self.urlParam = url_param
        self.cookie = cookies
        return url_param

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
        self.setUserInfo(username=username, password=password)
        response = self.loginAPI()
        return self.__checkAPI(response.history)

    def __login(self):
        """The concrete implementation of logining process. 
        """
        response = self.loginAPI()
        r_lsit = response.history

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
        assert response.status_code == 200
        return response

    def __checkAPI(self, res_history: list) -> bool:
        """Checking if the 'Set-Cookie' exist in the Headers to check out the userInfo. 
        """
        for each in res_history:
            if 'Set-Cookie' in each.headers:
                return True
        return False

    def __formatCookies(self, cookie: str) -> dict:
        if not cookie:
            return
        c1 = cookie.split(';')[0]
        cookies_list = c1.split('=')
        key = cookies_list[0]
        value = cookies_list[1]
        return {key: value}


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


if __name__ == "__main__":
    l_obj = Login('15122760', '1212CYZzy')
    cookie = l_obj.getCookie()
    print(cookie)
    # print(time())
    # print(l_obj.getUrlParam())
