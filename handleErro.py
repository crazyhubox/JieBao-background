from requests.exceptions import HTTPError
from Requets import PostRequest
from Reporter import AsyncReporter
from Requets.Login import ProxyLogin
from Proxy.proxy import Proxy
from Launcher import Actuator
from UserRedis import UserInfoRedis
from Launcher.Launcher import TroubleRemoval

import time

now = lambda :int(time.time())

def main():
    p = Proxy()
    accounts = UserInfoRedis()
    loginer = ProxyLogin(...,...)
    reporter = AsyncReporter()
    req_obj = PostRequest()
    
    while True:
        
        for each_p,t in p.getRawProxies():
            # print(each_p,t)
            # return 
            loginer.setProxy(each_p)
            req_obj.setProxy(each_p)
            launch = TroubleRemoval(accounts=accounts,loginer=loginer,requester=req_obj,reporter=reporter)
            try:
                # launch.Sun_Moon()
                launch.Total()
            except HTTPError as h:
                print(h.args,'==============')
                accounts.recoverErroUer()
                '''检查t'''
                if checkTimeout(t):
                    '''重新提取'''
                    p.Extract()
                    break
                else:
                    continue
            else:
                return
        if p.Scan() or not p.rdb.hlen(p.RawProxiesTable):
            p.Extract()


def checkTimeout(left_time:str)->bool:
    left_time = int(left_time)
    now_time = now()
    print(now_time,left_time)
    return True if now_time >= left_time else False

if __name__ == "__main__":
    main()
    # test_t = '1610174351'
    # res = checkTimeout(test_t)
    # print(res)
    # while True:
    #     print(now())
    #     time.sleep(1)
# statr = l_obj.getViewState()
# print(cookie)
# print(statr)
# reqer = PostRequest(cookie,statr,proxy=proxy)
# reper = AsyncReporter(reqer)
# reper.PreviousReport('2021-01-01')