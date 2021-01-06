from GetCookies import Login,getViewState
from Requets import PostRequest
from Reporter import Reporter
import schedule
from time import sleep
from datetime import date,datetime,timedelta
from UserRedis import UserInfoRedis


class Launcher:
    
    def __init__(self,accounts:UserInfoRedis, loginer:Login, requester:PostRequest, reporter:Reporter,):
        self.accounts = accounts
        self.loginer = loginer
        self.requester = requester
        self.reporter = reporter
        self.today = date.today()
        
        
    def Sun_Moon(self,flag):
        for user, passw in self.accounts.ReadUserInfo():
            print('[INFO]:',user)
            self.loginer.setUserInfo(username=user,password=passw)

            try:
                cookies = self.loginer.getCookie()
                view_state = getViewState(cookies)
                self.requester.setUserInfo(cookies,view_state)
                self.reporter.setRequester(self.requester)
                # self.reporter.PreviousReport('2020-12-10')
                if flag:
                    self.reporter.SunReport(self.today)
                else:
                    self.reporter.MoonRepot(self.today)
                print('='*100)
            except ValueError as e:
                if e.args[0] == '[ERROR]: UserInfo ERROR.':
                    self.accounts.removeErrorUser()
                    continue
            except:
                self.accounts.recoverErroUer()
            sleep(10)
        print('[Finished]:',datetime.now())


    def NewUser(self):
        for user,passw,each in self.accounts.getNewUser():
            print(F'[INFO]: NEW_USER -- {user}')
            self.loginer.setUserInfo(username=user,password=passw)
            cookies = self.loginer.getCookie()
            view_state = getViewState(cookies)
            self.requester.setUserInfo(cookies,view_state)
            self.reporter.setRequester(self.requester)
            self.reporter.SunReport(self.today)
            self.reporter.MoonRepot(self.today)
            print('='*100)
            self.accounts.saddUser(self.accounts.finishTables,each)
        else:
            # print('[Finished]:',datetime.now()) 
            pass

    def NewUserTotal(self):
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        for user,passw,each in self.accounts.getNewUser():
            print(F'[INFO]: NEW_USER -- {user}')
            self.loginer.setUserInfo(username=user,password=passw)
            cookies = self.loginer.getCookie()
            view_state = getViewState(cookies)
            self.requester.setUserInfo(cookies,view_state)
            self.reporter.setRequester(self.requester)
            self.reporter.PreviousReport(start_date)
            print('='*100)
            self.accounts.saddUser(self.accounts.finishTables,each)
        else:
            print(1)
            pass

    def schedule(self):
        schedule.every().day.at("06:30").do(self.Sun_Moon,flag=1)
        schedule.every().day.at("20:00").do(self.Sun_Moon,flag=0)
        # schedule.every().second.do(NewUser,*[self.today, self.accounts, self.loginer, self.requester, self.reporter])
        schedule.every().second.do(self.NewUserTotal)
        while True:
            schedule.run_pending()
            sleep(1)



if __name__ == "__main__":
    # main()
    # reporter = Launcher()
    print(date.today())
    # reporter.schedule()

