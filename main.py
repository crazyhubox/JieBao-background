from Launcher import Actuator
from Reporter import AsyncReporter
from UserRedis import UserInfoRedis
from Requets import Login,PostRequest

def main():
    accounts = UserInfoRedis()
    loginer = Login(...,...)
    req_obj = PostRequest()
    reporter = AsyncReporter()
    
    launch = Actuator(accounts=accounts,loginer=loginer,requester=req_obj,reporter=reporter)
    launch.schedule()
    # launch.Sun_Moon(1)
    # test_u = ''
    # test_p = ''
    # launch.dayReport(test_u,test_p)
    # launch.userPoll(test_u,test_p,'2020-12-07')

if __name__ == "__main__":
    main()