from requests.models import HTTPError
import schedule
from time import sleep
from datetime import date, datetime, timedelta
from ErroHandler.merry import MyMerry
import os
ERRORHANDLER = MyMerry()

class Launcher:
    def __init__(self, accounts, loginer, requester, reporter, ):
        self.accounts = accounts
        self.loginer = loginer
        self.requester = requester
        self.reporter = reporter
        ERRORHANDLER.setObject(self)
        
    def selectReport(self, user, passw, flag):
        today = date.today()
        self.loginer.setUserInfo(username=user, password=passw)
        cookies = self.loginer.getCookie()
        view_state = self.loginer.getViewState()
        print(cookies, view_state)
        self.requester.setUserInfo(cookies, view_state)
        self.reporter.setRequester(self.requester)
        if flag:
            self.reporter.SunReport(today)
        else:
            self.reporter.MoonRepot(today)

    def dayReport(self, user, passw):
        today = date.today()
        self.loginer.setUserInfo(username=user, password=passw)
        cookies = self.loginer.getCookie()
        view_state = self.loginer.getViewState()
        self.requester.setUserInfo(cookies, view_state)
        self.reporter.setRequester(self.requester)
        self.reporter.SunReport(today)
        self.reporter.MoonRepot(today)

    def userPoll(self, user, passw, start_date):
        self.loginer.setUserInfo(username=user, password=passw)
        cookies = self.loginer.getCookie()
        view_state = self.loginer.getViewState()
        self.requester.setUserInfo(cookies, view_state)
        self.reporter.setRequester(self.requester)
        self.reporter.PreviousReport(start_date)

    def schedule(self):
        pass


class Actuator(Launcher):
    def __init__(self, accounts, loginer, requester, reporter):
        super().__init__(accounts, loginer, requester, reporter)

    @ERRORHANDLER._try
    def selectReport(self, user, passw, flag):
        return super().selectReport(user, passw, flag)
    
    @ERRORHANDLER._except(ValueError)
    def handleValueError(self,e):
        if e.args[0] == '[ERROR]: UserInfo ERROR.':
            self.accounts.removeErrorUser()

    @ERRORHANDLER._except(KeyboardInterrupt)
    def handleKeyboardInterrupt(self,k):
        print(k.args)
        self.accounts.recoverErroUer()
        import os
        os._exit(0)#解释器直接退出

    @ERRORHANDLER._except(Exception)
    def handleException(self,e):
        print(e.args)
        self.accounts.recoverErroUer()
            
    
    def Sun_Moon(self, flag):
        """Complete the morning and evening reports of all users."""
        for user, passw in self.accounts.ReadUserInfo():
            print('[INFO]:', user)
            self.selectReport(user, passw, flag)
            print('=' * 100)
            sleep(10)
        print('[Finished]:', datetime.now())


    def NewUser(self):
        """Complete the morning and evening reports of one user."""
        for user, passw, each in self.accounts.getNewUser():
            print(F'[INFO]: NEW_USER -- {user}', datetime.now())
            self.dayReport(user, passw)
            print('=' * 100)
            self.accounts.saddUser(self.accounts.finishTables, each)
            # sleep()
        else:
            pass

    def NewUserTotal(self):
        """"Complete the reports of past 30 days."""
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        for user, passw, each in self.accounts.getNewUser():
            print(F'[INFO]: NEW_USER -- {user}', datetime.now())
            self.userPoll(user, passw, start_date)
            print('=' * 100)
            self.accounts.saddUser(self.accounts.finishTables, each)
        else:
            pass

    def schedule(self):
        schedule.every().day.at("06:30").do(self.Sun_Moon, flag=1)
        schedule.every().day.at("19:15").do(self.Sun_Moon, flag=0)
        # schedule.every().second.do(NewUser,*[self.today, self.accounts, self.loginer, self.requester, self.reporter])
        schedule.every().second.do(self.NewUserTotal)
        while True:
            schedule.run_pending()
            sleep(1)


class TroubleRemoval(Actuator):
    def __init__(self, accounts, loginer, requester, reporter):
        super().__init__(accounts, loginer, requester, reporter)

    @ERRORHANDLER._try
    def dayReport(self, user, passw):
        return super().dayReport(user, passw)


    def Sun_Moon(self):
        """Complete the morning and evening reports of all users."""
        for user, passw in self.accounts.ReadUserInfo():
            print('[INFO]:', user)
            self.dayReport(user, passw)
            print('=' * 100)
        print('[Finished]:', datetime.now())


    def Total(self):
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        for user, passw in self.accounts.ReadUserInfo():
            print('[INFO]:', user)
            self.userPoll(user, passw, start_date)
            print('=' * 100)
        else:
            pass
        print('[Finished]:', datetime.now())

if __name__ == "__main__":
    # main()
    # reporter = Launcher()
    print(date.today())
    # reporter.schedule()
