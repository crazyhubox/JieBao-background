from test import report
from .test import gen_url, datetime


class Reporter:
    def __init__(self, Requester=None) -> None:
        self.requester = Requester

    def setRequester(self, Requester):
        self.requester = Requester

    def PreviousReport(self, startDate: str):
        for each_date, t in gen_url(startDate):
            self.requester.report(each_date, t)

    def TodayReport(self):
        today = datetime.date.today()
        self.SunReport(today)
        self.MoonRepot(today)

    def SunReport(self, date: str):
        self.requester.report(date, 1)

    def MoonRepot(self, date: str):
        self.requester.report(date, 2)


class AsyncReporter(Reporter):
    def __init__(self, Requester=None) -> None:
        super().__init__(Requester=Requester)

    def PreviousReport(self,startDate):
        datas = []
        for each_date,t in  gen_url(start_date=startDate):
            datas.append((each_date,t))
        self.requester.asyncPost(datas)