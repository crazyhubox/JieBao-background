from Requets import PostRequest
from Reporter import AsyncReporter
from Requets.Login import ProxyLogin,Login

l_obj = ProxyLogin('19122044', 'Zxy011022')
cookie = l_obj.getCookie()
statr = l_obj.getViewState(cookie)
print(cookie)
print(statr)
reqer = PostRequest(cookie,statr)
reper = AsyncReporter(reqer)
reper.PreviousReport('2021-01-01')
