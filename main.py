# from GetCookies import GetCookies
from requests.models import HTTPError
from GetCookies import Login,getViewState
from Requets import PostRequest
from Reporter import Reporter
import schedule
from time import sleep
from datetime import date,datetime
from getUserFromRedis import UserInfoRedis

def main(t):    
    today = date.today()
    accounts = UserInfoRedis()
    loginer = Login(...,...)
    req_obj = PostRequest()
    reporter = Reporter()
    
    for user, passw in accounts.ReadUserInfo():
        print('[INFO]:',user)
        loginer.setUserInfo(username=user,password=passw)

        try:
            cookies = loginer.getCookie()
            view_state = getViewState(cookies)
            req_obj.setUserInfo(cookies,view_state)
            reporter.setRequester(req_obj)
            # reporter.PreviousReport('2020-12-31')
            if t:
                reporter.SunReport(today)
            else:
                reporter.MoonRepot(today)
            print('='*100)
        except:
            accounts.recoverErroUer()
            
        sleep(3)
    print('[Finished]:',datetime.now())


def run():
    schedule.every().day.at("07:30").do(main,t=1)
    schedule.every().day.at("20:00").do(main,t=0)

    while True:
        schedule.run_pending()
        sleep(1)


if __name__ == "__main__":
    for i in range(50):
        main(1)
    # run()

