from Reporter.reporter import VocattionReporter
from Requets.PostRequest import DayReportPost
from Requets.Login import LoginDayReport
from Launcher.Launcher import VocationActuator
import sys
import traceback

def vocation():
    loginer = LoginDayReport(...,...)
    requester = DayReportPost()
    reporter = VocattionReporter()
    launch = VocationActuator(None,loginer,requester,reporter)
    launch.schedule()


if __name__ == '__main__':
    try:
        vocation()
    except Exception as e:
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        traceback.print_tb(exc_traceback_obj)
        res:list = traceback.format_tb(exc_traceback_obj)
        res.append(type(e).__name__)
        if len(e.args):
            res.append(e.args[0])
        from Notification.send_email import send_erro
        send_erro(res)
        print(e.args)
