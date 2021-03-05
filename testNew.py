from Requets.Login import LoginDayReport
from Requets.PostRequest import DayReportPost

def main():
    l_obj = LoginDayReport(...,...)
    l_obj.setUserInfo('','')
    cookies = l_obj.getCookie()
    viewStatus = l_obj.getViewState()
    p_test = DayReportPost()
    p_test.setUserInfo(cookie=cookies,viewstate=viewStatus)
    p_test.report(date='2020-01-24')
    
    
if __name__ == '__main__':
    main()