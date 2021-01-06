from Launcher import Actuator,UserInfoRedis,Login,PostRequest,Reporter
from Reporter import AsyncReporter


def main():
    accounts = UserInfoRedis()
    loginer = Login(...,...)
    req_obj = PostRequest()
    # reporter = Reporter()
    reporter = AsyncReporter()
    launch = Actuator(accounts=accounts,loginer=loginer,requester=req_obj,reporter=reporter)
    launch.schedule()
    # launch.Sun_Moon(1)
    test_u = '16123113'
    test_p = '130E2d898'
    # launch.dayReport(test_u,test_p)
    # launch.userPoll(test_u,test_p,'2020-12-01')

if __name__ == "__main__":
    main()