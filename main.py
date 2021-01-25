from Launcher.Launcher import Actuator,VocationActuator
from Reporter import AsyncReporter
from UserRedis import UserInfoRedis
from Requets import Login,PostRequest,ProxyLogin
import sys
import traceback



def main():
    accounts = UserInfoRedis()
    loginer = Login(...,...)
    # loginer = ProxyLogin(...,...)
    # loginer.setProxies(loginer.headers.proxies())
    req_obj = PostRequest()
    reporter = AsyncReporter()
    
    launch = Actuator(accounts=accounts,loginer=loginer,requester=req_obj,reporter=reporter)
    launch.schedule()
    # launch.NewUserTotal()
    # launch.Sun_Moon(0)    
    # launch.userPoll()
    # test_u = ''
    # test_p = ''
    # launch.dayReport(test_u,test_p)
    # launch.userPoll(test_u,test_p,'2020-12-07')




if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        traceback.print_tb(exc_traceback_obj)

        res:list = traceback.format_tb(exc_traceback_obj)

        # res.append(type(e).__name__)
        # if len(e.args):
        #     res.append(e.args[0])
        # from Notification.send_email import send_erro
        # send_erro(res)
        print('='*100)
        print(e.args)
        
    
    